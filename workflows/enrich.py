"""Contact enrichment workflow."""

import logging

logger = logging.getLogger(__name__)


async def run(contact_id: str) -> None:
    """
    Enrich a newly created contact with additional data.

    This workflow is triggered when a new contact is created in HubSpot.
    It will fetch additional information about the contact and update their record.

    Args:
        contact_id: The HubSpot contact ID to enrich
    """
    logger.info(f"Enrich workflow called for contact_id: {contact_id}")
    # TODO: Implement contact enrichment logic
    pass
