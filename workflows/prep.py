"""Deal preparation workflow."""

import logging

logger = logging.getLogger(__name__)


async def run(deal_id: str) -> None:
    """
    Prepare materials and briefing for a deal stage change.

    This workflow is triggered when a deal moves to a new stage.
    It prepares relevant materials, talking points, and notifications
    for the sales team.

    Args:
        deal_id: The HubSpot deal ID to prepare for
    """
    logger.info(f"Prep workflow called for deal_id: {deal_id}")
    # TODO: Implement deal preparation logic
    pass
