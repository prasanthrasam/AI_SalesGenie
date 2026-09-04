# Observability and Evaluation Strategy

## Selected tool

SalesGenie uses Langfuse for external LLM observability, supplemented by Langflow Native Traces. Langfuse ingestion has been verified in the US-region dashboard: complete flow observations are visible for Prompt Template, Structured Output/model processing, Catalog Guard, Follow-Up Draft Model, and Chat Output.

## Trace evidence to capture

- End-to-end status and duration for the Catalog Recommender flow
- Prompt Template input/output
- Structured Output input/output
- OpenAI model name, latency, and token usage when available
- Catalog Guard input/output and rejected recommendations
- Follow-Up Draft Model input/output, latency, and token usage
- Weekly Sales Aggregator input/output and duration

## Evaluation metrics

- Baseline pass rate across T1-T11
- Message-routing accuracy
- Lead-tier accuracy
- Catalog-grounding accuracy
- Hard-budget compliance
- Hallucination count
- Average end-to-end latency per inquiry
- Input and output tokens per inquiry
- Estimated model cost per processed lead

## Known findings

- Prompt-only catalog enforcement included an over-budget product and transferred a finish between product rows.
- A deterministic Catalog Guard removed invalid products and rebuilt product facts from exact CSV rows.
- Vague and competitor inquiries required deterministic route corrections.
- Follow-up drafting required the original inquiry to identify customer requirements absent from structured extraction.

## Recorded trace

- Test: Cold-lead follow-up asking for missing furniture type, budget, and quantity
- Result: Passed; the email requested exactly those fields and invented no products or customer details
- Model: `gpt-4o-mini`
- Langfuse trace ID: `096f5e6f3a4ea643f3a08dcd908e875f`
- Langflow graph run ID: `e582304c-ded2-4d52-a33c-4a96a93c872c`
- Drafting-call usage: 3,063 input tokens, 231 output tokens, 3,294 total tokens
- Estimated drafting-call cost: $0.000598 (about $0.00060), using $0.15/M input tokens and $0.60/M output tokens
- Scope note: this is the Follow-Up Draft Model call only. Add the Structured Output span usage to calculate the complete flow cost per lead.
- Dashboard verification: Passed on 2026-09-03. The Langfuse Tracing table displayed the complete component sequence and model observations after a fresh Langflow run.

## Privacy

Traces can contain customer emails, inquiry text, and model responses. Use synthetic evaluation records, restrict trace access, redact personal data before screenshots, and define a retention period before rollout.
