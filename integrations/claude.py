"""Claude AI integration for intelligent assistance."""

from typing import Optional
from config import config


async def ask_claude(prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
    """
    Send a prompt to Claude and get a response.

    Args:
        prompt: The user prompt to send to Claude
        system_prompt: Optional system prompt to guide Claude's behavior

    Returns:
        Claude's response text or None if request fails
    """
    # TODO: Implement Anthropic API call to Claude
    pass
