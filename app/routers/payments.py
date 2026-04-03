from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class PaymentRequest(BaseModel):
    amount: float
    currency: str = "USD"
    description: str = ""


class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str


@router.post("/", response_model=PaymentResponse)
async def create_payment(payment: PaymentRequest) -> PaymentResponse:
    """Create a new payment."""
    if payment.amount <= 0:
        raise HTTPException(status_code=422, detail="Amount must be positive")

    return PaymentResponse(
        payment_id="pay_abc123",
        status="pending",
        amount=payment.amount,
        currency=payment.currency,
    )


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: str) -> PaymentResponse:
    """Retrieve payment by ID."""
    return PaymentResponse(
        payment_id=payment_id,
        status="completed",
        amount=100.0,
        currency="USD",
    )
