"""
Webhook tests.

FAULT: test_payment_webhook uses time.sleep for synchronisation.
This causes random failures on loaded CI runners because the async
callback may take longer than 100 ms.

Fix (Part 3): rewrite with pytest-asyncio and await.
"""
import time
from app.services.webhook import process_webhook_event


# --- FAULT: flaky timer-based test ---
def test_payment_webhook():
    import asyncio

    loop = asyncio.new_event_loop()
    result = None

    def run():
        nonlocal result
        result = loop.run_until_complete(
            process_webhook_event("payment.completed", 100)
        )

    import threading
    t = threading.Thread(target=run)
    t.start()

    time.sleep(0.1)   # FAULT: race condition — may not be enough under load

    assert result == "processed", f"expected 'processed', got {result!r}"
    t.join()


# --- Additional deterministic tests (these are fine) ---
def test_refund_webhook():
    import asyncio
    result = asyncio.run(process_webhook_event("refund.requested", 50))
    assert result == "refunded"


def test_unknown_event():
    import asyncio
    result = asyncio.run(process_webhook_event("subscription.created", 0))
    assert result == "ignored"
