# Langfuse Trace Evidence

These screenshots document a successful end-to-end SalesGenie Catalog Recommender run in Langfuse.

| File | Evidence |
|---|---|
| `01-tracing-overview.png` | Complete Langflow component observations received by Langfuse |
| `02-router-model-usage.png` | Router/extractor model, latency, token usage, and cost |
| `03-catalog-guard-input.png` | Structured result and catalog data supplied to the deterministic guard |
| `04-catalog-guard-output.png` | Grounded P002/P003 recommendations, prices, and availability |
| `05-follow-up-model-usage.png` | Follow-up model input, model version, latency, tokens, and cost |
| `06-follow-up-email-output.png` | Final grounded email with validated products, prices, availability, and the unconfirmed-finish notice |
| `07-manual-overall-pass-score.png` | Human evaluation attached to the trace and observation with `overall_pass: True` |
| `08-spam-catalog-guard-output.png` | Spam edge case with empty recommendations and explicit no-sales-action response |
| `09-spam-overall-pass-score.png` | Human `overall_pass: True` evaluation attached to the spam trace and guard observation |

Observed model-call totals for this run:

- Router/extractor: 2,655 tokens, $0.000532, 3.67 seconds
- Follow-up drafting: 1,117 tokens, $0.000255, 2.73 seconds
- Combined: 3,772 tokens, $0.000787, 6.40 seconds of model latency
