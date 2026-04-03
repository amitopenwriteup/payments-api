import asyncio


async def process_webhook_event(event: str, amount: float) -> str:
    """
    Process an incoming webhook event asynchronously.
    Simulates async I/O (e.g. database write, downstream notification).
    """
    await asyncio.sleep(0)  # yield control — simulates real async work

    if event.startswith("payment."):
        return "processed"
    elif event.startswith("refund."):
        return "refunded"
    else:
        return "ignored"
