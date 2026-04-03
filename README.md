# payments-api

Sample FastAPI service used in the **AI in CI/CD Pipelines** lab workshop (Module 1).

## Deliberate Faults

Three faults have been seeded for the lab exercises:

| # | File | Fault | Lab Part |
|---|------|-------|----------|
| 1 | `pyproject.toml` | `httpx==0.24.0` conflicts with `fastapi 0.110` at runtime | Part 1 |
| 2 | `tests/test_webhooks.py` | `test_payment_webhook` uses `time.sleep` — flaky under CI load | Part 3 |
| 3 | `k8s/rollout.yaml` | `maxUnavailable: 100%` and no `AnalysisTemplate` | Part 4 |

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Reproduce fault 1
python -c "from app.main import app"

# Run tests (observe flaky fault 2)
for i in {1..10}; do pytest tests/test_webhooks.py::test_payment_webhook -x -q 2>&1 | tail -1; done
```

## Repository Structure

```
payments-api/
├── app/
│   ├── main.py                        # FastAPI app factory
│   ├── routers/
│   │   ├── payments.py                # Payment endpoints
│   │   └── webhooks.py                # Webhook endpoints
│   └── services/
│       └── webhook.py                 # Async webhook processing
├── tests/
│   ├── conftest.py                    # Shared fixtures (async_client)
│   ├── test_payments.py               # Payment route tests
│   └── test_webhooks.py               # Webhook tests (contains flaky fault)
├── k8s/
│   ├── rollout.yaml                   # Argo Rollout (contains deploy faults)
│   ├── service.yaml                   # Stable + canary services
│   └── analysis-template.yaml        # Prometheus AnalysisTemplate (Part 4 fix)
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                     # Main CI pipeline
│   │   └── ai-review.yml              # AI code review gate (Part 2)
│   └── scripts/
│       ├── llm_review.py              # Anthropic API review script
│       └── select_tests.sh            # Heuristic test selector (Part 3)
├── pyproject.toml                     # Dependencies (contains httpx fault)
└── renovate.json                      # Renovate config with FastAPI group rule
```

## Secrets Required

| Secret | Used in |
|--------|---------|
| `ANTHROPIC_API_KEY` | `ai-review.yml` — Part 2 |
| `LAUNCHABLE_TOKEN` | `ci.yml` — Part 3 (optional) |
