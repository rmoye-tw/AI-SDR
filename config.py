"""Configuration settings for the BDR Assistant application."""

import os
from typing import Optional


class Config:
    """Application configuration loaded from environment variables."""

    # API Keys and Tokens
    HUBSPOT_API_KEY: Optional[str] = os.getenv("HUBSPOT_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    SLACK_BOT_TOKEN: Optional[str] = os.getenv("SLACK_BOT_TOKEN")

    # HubSpot Configuration
    HUBSPOT_PORTAL_ID: Optional[str] = os.getenv("HUBSPOT_PORTAL_ID")

    # Workflow Constants
    HIGH_PRIORITY_SCORE: int = 7


# Global config instance
config = Config()
