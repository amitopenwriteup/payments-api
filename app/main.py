from fastapi import FastAPI
from app.routers import payments, webhooks

app = FastAPI(
    title="Payments API",
    description="FastAPI service for processing payments and webhooks",
    version="0.1.0",
)

app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
