"""Event routing logic for HubSpot webhooks."""

import logging
from typing import Dict, Any
from workflows import enrich, draft, prep, followup
from integrations.slack import post_error

logger = logging.getLogger(__name__)


async def route_event(payload: Dict[str, Any]) -> None:
    """
    Route a HubSpot webhook event to the appropriate workflow handler.

    Args:
        payload: The HubSpot webhook payload containing event data

    Routes based on subscriptionType:
        - contact.creation -> enrich workflow
        - contact.propertyChange -> draft or followup workflow (based on property)
        - deal.propertyChange -> prep workflow (for dealstage changes)
    """
    try:
        subscription_type = payload.get("subscriptionType")

        if not subscription_type:
            logger.warning(f"Webhook payload missing subscriptionType: {payload}")
            return

        logger.info(f"Routing event: {subscription_type}")

        # Handle contact creation events
        if subscription_type == "contact.creation":
            contact_id = payload.get("objectId")
            if contact_id:
                await enrich.run(contact_id)
            else:
                logger.error(f"Contact creation event missing objectId: {payload}")

        # Handle contact property change events
        elif subscription_type == "contact.propertyChange":
            contact_id = payload.get("objectId")
            property_name = payload.get("propertyName")

            if not contact_id:
                logger.error(f"Contact property change missing objectId: {payload}")
                return

            # Route based on which property changed
            if property_name in ["lifecyclestage", "lead_status", "hs_lead_status"]:
                # Contact ready for outreach - draft email
                await draft.run(contact_id)
            elif property_name in ["notes_last_updated", "engagement_last_updated", "email_opened", "email_clicked"]:
                # Contact engagement - trigger follow-up
                await followup.run(contact_id)
            else:
                logger.info(f"Unhandled property change: {property_name} for contact {contact_id}")

        # Handle deal property change events
        elif subscription_type == "deal.propertyChange":
            deal_id = payload.get("objectId")
            property_name = payload.get("propertyName")

            if not deal_id:
                logger.error(f"Deal property change missing objectId: {payload}")
                return

            # Only handle dealstage changes
            if property_name == "dealstage":
                await prep.run(deal_id)
            else:
                logger.info(f"Unhandled deal property change: {property_name} for deal {deal_id}")

        else:
            logger.warning(f"Unhandled subscription type: {subscription_type}")

    except Exception as e:
        error_msg = f"Error routing event: {str(e)}"
        logger.error(error_msg, exc_info=True)

        # Post error to Slack for visibility
        try:
            await post_error(error_msg, context={"payload": payload})
        except Exception as slack_error:
            logger.error(f"Failed to post error to Slack: {slack_error}")
