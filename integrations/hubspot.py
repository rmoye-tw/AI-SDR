"""HubSpot API integration for managing contacts and deals."""

from typing import Optional, Dict, Any, List
import httpx
from config import config

# HubSpot API base URL
HUBSPOT_API_BASE = "https://api.hubapi.com"


def _get_headers() -> Dict[str, str]:
    """
    Get the authorization headers for HubSpot API requests.

    Returns:
        Dictionary with Authorization header
    """
    return {
        "Authorization": f"Bearer {config.HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }


async def get_contact(contact_id: int) -> dict:
    """
    Retrieve a contact from HubSpot by ID.

    Args:
        contact_id: The HubSpot contact ID

    Returns:
        Contact data dictionary with properties and metadata

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> contact = await get_contact(12345)
        >>> print(contact['properties']['email'])
    """
    properties = [
        "email",
        "firstname",
        "lastname",
        "company",
        "phone",
        "jobtitle",
        "hs_lead_status"
    ]

    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/contacts/{contact_id}"
    params = {"properties": ",".join(properties)}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=_get_headers(), params=params)
        response.raise_for_status()
        return response.json()


async def update_contact(contact_id: int, properties: dict) -> dict:
    """
    Update a contact's properties in HubSpot.

    Args:
        contact_id: The HubSpot contact ID
        properties: Dictionary of properties to update

    Returns:
        Updated contact data dictionary

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> updated = await update_contact(12345, {
        ...     "hs_lead_status": "QUALIFIED",
        ...     "jobtitle": "Senior Engineer"
        ... })
    """
    # Filter out None values
    filtered_properties = {k: v for k, v in properties.items() if v is not None}

    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/contacts/{contact_id}"
    payload = {"properties": filtered_properties}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=_get_headers(), json=payload)
        response.raise_for_status()
        return response.json()


async def get_deal(deal_id: int) -> dict:
    """
    Retrieve a deal from HubSpot by ID.

    Args:
        deal_id: The HubSpot deal ID

    Returns:
        Deal data dictionary with properties, metadata, and contact associations

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> deal = await get_deal(67890)
        >>> print(deal['properties']['dealname'])
        >>> print(deal['associations']['contacts'])
    """
    properties = ["dealname", "dealstage", "amount", "closedate"]

    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/deals/{deal_id}"
    params = {
        "properties": ",".join(properties),
        "associations": "contacts"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=_get_headers(), params=params)
        response.raise_for_status()
        return response.json()


async def get_contact_by_email(email: str) -> Optional[dict]:
    """
    Search for a contact by email address.

    Args:
        email: The email address to search for

    Returns:
        Contact data dictionary if found, None if not found

    Raises:
        httpx.HTTPStatusError: If the API request fails (except 404)

    Example:
        >>> contact = await get_contact_by_email("john@example.com")
        >>> if contact:
        ...     print(f"Found contact: {contact['id']}")
    """
    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/contacts/search"
    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email
                    }
                ]
            }
        ],
        "properties": [
            "email",
            "firstname",
            "lastname",
            "company",
            "phone",
            "jobtitle",
            "hs_lead_status"
        ],
        "limit": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=_get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            return data["results"][0]
        return None


async def get_recent_engagements(contact_id: int, limit: int = 10) -> list:
    """
    Fetch recent engagements (emails, calls, meetings) for a contact.

    Args:
        contact_id: The HubSpot contact ID
        limit: Maximum number of engagements to return (default: 10)

    Returns:
        List of engagement objects sorted by most recent

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> engagements = await get_recent_engagements(12345, limit=5)
        >>> for engagement in engagements:
        ...     print(f"{engagement['type']}: {engagement['timestamp']}")
    """
    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/contacts/{contact_id}/associations/engagements"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=_get_headers())
        response.raise_for_status()
        data = response.json()

        # Get the engagement IDs
        engagement_ids = [result["id"] for result in data.get("results", [])]

        if not engagement_ids:
            return []

        # Fetch engagement details (limited to the requested number)
        engagement_ids = engagement_ids[:limit]
        engagements = []

        for engagement_id in engagement_ids:
            try:
                engagement_url = f"{HUBSPOT_API_BASE}/crm/v3/objects/engagements/{engagement_id}"
                engagement_response = await client.get(engagement_url, headers=_get_headers())
                engagement_response.raise_for_status()
                engagements.append(engagement_response.json())
            except httpx.HTTPStatusError:
                # Skip engagements that fail to fetch
                continue

        return engagements


async def search_contacts(
    filters: list,
    properties: Optional[list] = None,
    limit: int = 100
) -> list:
    """
    Generic search function using HubSpot's search API.

    Args:
        filters: List of filter groups in HubSpot's filter format
        properties: List of property names to include (default: common properties)
        limit: Maximum number of contacts to return (default: 100)

    Returns:
        List of matching contact objects

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> # Search for qualified leads in technology
        >>> filters = [
        ...     {
        ...         "filters": [
        ...             {"propertyName": "hs_lead_status", "operator": "EQ", "value": "QUALIFIED"},
        ...             {"propertyName": "industry", "operator": "EQ", "value": "TECHNOLOGY"}
        ...         ]
        ...     }
        ... ]
        >>> contacts = await search_contacts(filters, limit=50)
        >>> print(f"Found {len(contacts)} qualified tech contacts")
    """
    if properties is None:
        properties = [
            "email",
            "firstname",
            "lastname",
            "company",
            "phone",
            "jobtitle",
            "hs_lead_status"
        ]

    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/contacts/search"
    payload = {
        "filterGroups": filters,
        "properties": properties,
        "limit": limit
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=_get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
