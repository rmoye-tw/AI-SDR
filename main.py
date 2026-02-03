"""FastAPI application for BDR workflow orchestration."""

import logging
from typing import Dict, Any
from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from router import route_event

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BDR Assistant",
    description="AI-powered BDR workflow orchestration system",
    version="1.0.0"
)


@app.get("/")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Status message indicating the service is running
    """
    return {"status": "healthy", "service": "BDR Assistant"}


@app.post("/webhook/hubspot")
async def hubspot_webhook(
    request: Request,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Receive and process HubSpot webhook events.

    This endpoint receives webhook payloads from HubSpot and routes them
    to appropriate workflow handlers. Processing happens in the background
    to avoid webhook timeouts.

    Args:
        request: The incoming HTTP request containing the webhook payload
        background_tasks: FastAPI background tasks handler

    Returns:
        JSON response acknowledging receipt of the webhook
    """
    try:
        # Parse the incoming webhook payload
        payload: Dict[str, Any] = await request.json()

        logger.info(f"Received HubSpot webhook: {payload.get('subscriptionType')}")

        # Process the event in the background to avoid timeout
        background_tasks.add_task(route_event, payload)

        return JSONResponse(
            status_code=200,
            content={"status": "received", "message": "Webhook processing started"}
        )

    except Exception as e:
        logger.error(f"Error processing HubSpot webhook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process webhook"
        )


@app.post("/webhook/slack")
async def slack_webhook(
    request: Request,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Receive and process Slack webhook events.

    This endpoint is a placeholder for future Slack interactions such as
    slash commands, button clicks, or other interactive components.

    Args:
        request: The incoming HTTP request containing the Slack payload
        background_tasks: FastAPI background tasks handler

    Returns:
        JSON response acknowledging receipt of the event
    """
    try:
        payload: Dict[str, Any] = await request.json()

        logger.info(f"Received Slack webhook: {payload.get('type')}")

        # TODO: Implement Slack event routing and handling

        return JSONResponse(
            status_code=200,
            content={"status": "received", "message": "Slack event received"}
        )

    except Exception as e:
        logger.error(f"Error processing Slack webhook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process Slack webhook"
        )


if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
