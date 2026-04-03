from fastapi import APIRouter
from pydantic import BaseModel
from app.services.webhook import process_webhook_event

router = APIRouter()


class WebhookPayload(BaseModel):
    event: str
    amount: float = 0.0
    #metadata: dict = {}
    metadata: dict[str, object] = {}

class WebhookResponse(BaseModel):
    status: str
    event: str


@router.post("/payment", response_model=WebhookResponse)
async def payment_webhook(payload: WebhookPayload) -> WebhookResponse:
    """Receive and process a payment webhook event."""
    result = await process_webhook_event(payload.event, payload.amount)
    return WebhookResponse(status=result, event=payload.event)
