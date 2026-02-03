"""Email draft generation workflow."""

import logging

logger = logging.getLogger(__name__)


async def run(contact_id: str) -> None:
    """
    Generate a draft email for a contact.

    This workflow is triggered when a contact property changes indicating
    they are ready for outreach. It uses Claude to generate a personalized
    email draft.

    Args:
        contact_id: The HubSpot contact ID to draft email for
    """
    logger.info(f"Draft workflow called for contact_id: {contact_id}")
    # TODO: Implement email draft generation logic
    pass
