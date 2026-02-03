"""Follow-up workflow for contact engagement."""

import logging

logger = logging.getLogger(__name__)


async def run(contact_id: str) -> None:
    """
    Handle follow-up actions for a contact.

    This workflow is triggered when a contact property changes indicating
    they require follow-up (e.g., email opened, link clicked, meeting scheduled).
    It determines the appropriate next action and executes it.

    Args:
        contact_id: The HubSpot contact ID to follow up with
    """
    logger.info(f"Followup workflow called for contact_id: {contact_id}")
    # TODO: Implement follow-up logic
    pass
