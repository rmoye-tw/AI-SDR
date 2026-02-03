# BDR Assistant

An AI-powered Business Development Representative (BDR) workflow orchestration system that automates contact enrichment, email drafting, deal preparation, and follow-ups using HubSpot, Claude AI, and Slack integrations.

## Project Structure

```
AI-SDR/
├── main.py                 # FastAPI application entry point
├── router.py               # Event routing logic
├── config.py               # Configuration and environment variables
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── integrations/           # External service integrations
│   ├── __init__.py
│   ├── hubspot.py         # HubSpot API client
│   ├── claude.py          # Claude AI client
│   └── slack.py           # Slack API client
└── workflows/             # Workflow handlers
    ├── __init__.py
    ├── enrich.py          # Contact enrichment workflow
    ├── draft.py           # Email draft generation workflow
    ├── prep.py            # Deal preparation workflow
    └── followup.py        # Follow-up workflow
```

## Features

- **Webhook Processing**: Receives and processes HubSpot webhooks asynchronously
- **Event Routing**: Routes events to appropriate workflows based on subscription type
- **Workflow Automation**:
  - Contact enrichment on creation
  - Email draft generation for qualified leads
  - Deal preparation for stage changes
  - Automated follow-ups based on engagement
- **Error Handling**: Comprehensive logging and Slack error notifications
- **Background Processing**: Non-blocking webhook processing to prevent timeouts

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Fill in your API keys and credentials in the `.env` file

## Running the Application

Start the FastAPI server:

```bash
python main.py
```

The server will run on `http://0.0.0.0:8080`

## Endpoints

- `GET /` - Health check endpoint
- `POST /webhook/hubspot` - Receives HubSpot webhook events
- `POST /webhook/slack` - Placeholder for Slack interactions (future use)

## Event Routing

The application routes HubSpot events as follows:

| Event Type | Property | Workflow |
|------------|----------|----------|
| `contact.creation` | - | `enrich` |
| `contact.propertyChange` | `lifecyclestage`, `lead_status` | `draft` |
| `contact.propertyChange` | `email_opened`, `email_clicked` | `followup` |
| `deal.propertyChange` | `dealstage` | `prep` |

## Next Steps

1. Implement the integration stubs in `integrations/` directory
2. Implement workflow logic in `workflows/` directory
3. Set up HubSpot webhook subscriptions
4. Configure Slack channels for notifications
5. Add authentication/verification for webhook endpoints

## Development

This application uses:
- **FastAPI** for the web framework
- **httpx** for async HTTP requests
- **uvicorn** for ASGI server
- **pydantic** for data validation
