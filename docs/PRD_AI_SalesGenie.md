# Product Requirements Document

## AI SalesGenie

Functional and technical specification for the Langflow implementation

| Organization | Oak & Ember Interiors |
| --- | --- |
| Document owner | AI Product / Technical Program Management |
| Version | 1.0 |
| Date | September 4, 2026 |
| Status | Final capstone submission |


# 1. Product Overview

AI SalesGenie is a low-code, agentic sales assistant for Oak & Ember Interiors. It processes inbound inquiry text through a router and structured extractor, grounds recommendations in a CSV catalog, validates proposed recommendations with deterministic Python logic, drafts a customer response, and separately summarizes CRM records. The implementation uses Langflow, OpenAI gpt-4o-mini, custom Python components, and Langfuse.


# 2. Product Goals and Non-Goals


## 2.1 Goals

- Convert unstructured sales messages into consistent structured records.
- Route inquiries safely and qualify only valid leads.
- Return catalog-grounded and budget-compliant recommendations.
- Draft useful follow-up emails with transparent limitations.
- Produce deterministic weekly metrics from source CRM rows.
- Make execution quality, latency, tokens, and cost observable.

## 2.2 Non-goals

- Direct production email delivery or autonomous CRM mutation.
- Order management, inventory reservation, payment, or fulfillment.
- Open-web product research or unsupported competitor claims.
- Fine-tuning or production-scale retrieval infrastructure in the initial release.

# 3. Users and Key Journeys

| Persona | Need | Primary journey |
| --- | --- | --- |
| Sales representative | Quickly understand and respond to inquiries | Submit message, review qualification/recommendations, approve draft |
| Sales manager | Consistent pipeline insight | Review weekly summary and quality/cost metrics |
| Sales operations | Structured and traceable records | Validate schemas, exports, and source traceability |
| AI PM/TPM | Reliable and governable workflow | Evaluate traces, scores, failures, cost, and regressions |


# 4. Architecture and Orchestration

The product uses a sequential pipeline with routing decisions embedded at the extraction stage. Every customer message follows a predictable path, while non-sales routes receive deterministic handling. Weekly aggregation runs as a separate flow because it uses batch CRM records rather than a single inquiry.

1. Chat Input captures the inquiry.
1. Prompt Template combines routing/extraction rules, catalog context, and inbound text.
1. Structured Output uses gpt-4o-mini at temperature 0 to produce the typed record.
1. Catalog Guard validates the result against raw CSV, enforces budget and stock rules, and rebuilds factual claims.
1. Follow-Up Email Prompt combines the validated record with the original inquiry.
1. Follow-Up Draft Model uses gpt-4o-mini at temperature 0.2 to produce a draft-only response.
1. Chat Output displays the result.
1. The separate Weekly Sales Aggregator calculates deterministic summary statistics from CRM CSV rows.

# 5. Functional Requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| FR-01 | Accept inquiry text through Langflow Chat Input. | All inquiry tests |
| FR-02 | Classify message_type as sales inquiry, product question, stock question, competitor comparison, complaint, spam, or weekly-summary request. | T1-T11 routing expectations |
| FR-03 | Extract customer name, email, company, product interest, budgets, quantity, urgency, deadline, requirements, and competitor mentions. | Structured fields match explicit evidence |
| FR-04 | Assign Hot/Warm/Cold only to sales inquiries. | T1/T3/T5/T8 and vague cases |
| FR-05 | Return aligned arrays for recommendation IDs, names, prices, availability, and rationales. | Array lengths match and values are typed |
| FR-06 | Validate every recommendation against the exact catalog row. | No unknown ID/name or cross-row feature attribution |
| FR-07 | Reject products over budget or unavailable for recommendation. | guard_rejections records the reason |
| FR-08 | Answer named product and stock questions from exact catalog data. | T4 and T10 |
| FR-09 | Generate no recommendations for spam and vague inquiries lacking essential information. | T2/T7/T9 |
| FR-10 | Draft a response using only validated product facts and original customer requirements. | Extended-capability tests |
| FR-11 | Calculate weekly totals, tier/category breakdowns, top categories, average known budget, and source IDs. | T11 |
| FR-12 | Emit Langfuse traces for model and component observations. | Trace and score evidence |


# 6. Data Contract

| Field group | Representative fields | Rules |
| --- | --- | --- |
| Routing | message_type, classification_reason | Use allowed route values; state evidence concisely |
| Identity | customer_name, email, company | Extract only explicit identity; normalize formatted email |
| Commercial | product_interest, budget_total, budget_per_unit, quantity | Use numeric zero only when unknown; do not infer unsupported values |
| Qualification | urgency, deadline_text, lead_tier, missing_information | No tier for non-leads; list actionable missing fields |
| Recommendations | IDs, names, prices, availability, rationales | Aligned arrays; exact catalog values; one to three products |
| Response | response_text, catalog_grounded, guard_rejections | Transparent response and deterministic validation audit trail |


# 7. Product and Validation Rules

- Catalog Guard is authoritative for recommendation IDs, names, prices, availability, and descriptions.
- A total budget with quantity is converted to a per-unit ceiling for product selection.
- A standing-desk request matches desk-category products and excludes accessories such as standing mats.
- Product questions may return a factual response without recommendation arrays.
- Stock questions report catalog status and never fabricate a restock date.
- Cold vague inquiries return direct clarification questions.
- Spam returns no products and an explicit no-sales-action message.
- The follow-up model must not add marketing superlatives, warranties, discounts, delivery commitments, or feature claims not present in validated data.

# 8. Non-Functional Requirements

| Area | Requirement |
| --- | --- |
| Reliability | A component failure must be visible and must not silently produce an unvalidated customer response. |
| Performance | Target median end-to-end pilot latency below 10 seconds, excluding file upload and operator review. |
| Cost | Record per-model tokens and cost; alert on unexpected growth in context or completion length. |
| Security | Keep API keys in environment variables; exported JSON and Git history must contain no secrets. |
| Privacy | Restrict trace access, prefer synthetic data, redact customer identifiers in shared evidence, and define retention. |
| Maintainability | Version prompts, schemas, custom components, data samples, exports, and evaluation results in Git. |
| Auditability | Preserve trace IDs, guard rejection reasons, source lead IDs, test results, and human scores. |


# 9. Evaluation and Acceptance

The mandatory T1-T11 dataset is the release regression suite. Current implementation results record all eleven required behaviors as passed, with cleanup observations retained where appropriate. Langfuse evidence confirms trace ingestion and human scoring for a grounded recommendation and a spam edge case.

| Evaluation dimension | Method | Acceptance threshold |
| --- | --- | --- |
| Routing accuracy | Compare message_type and tier with T1-T11 expectations | All mandatory cases correct |
| Catalog grounding | Match every recommendation claim to product_catalog.csv | 100%; zero invented products |
| Budget compliance | Compare selected price with total/per-unit ceiling | 100% |
| Hallucination | Review unsupported products, features, prices, stock, and restock claims | Zero critical hallucinations |
| Follow-up quality | Human review for accuracy, completeness, tone, and next action | Pass / acceptable with minor edits |
| Observability | Verify traces, model metadata, latency, tokens, cost, and manual score | Evidence retained for representative runs |


# 10. Cost and Performance Evidence

For the retained standing-desk run, the router/extractor used 2,655 tokens, cost $0.000532, and took 3.67 seconds. The follow-up model used 1,117 tokens, cost $0.000255, and took 2.73 seconds. Combined model usage was 3,772 tokens at $0.000787 with 6.40 seconds of model latency. These figures are trace-specific and should be aggregated across representative production traffic before forecasting.


# 11. Dependencies and Configuration

| Dependency | Purpose | Configuration |
| --- | --- | --- |
| Langflow | Workflow orchestration and custom components | Local runtime; exported JSON flows |
| OpenAI gpt-4o-mini | Structured extraction and follow-up drafting | OPENAI_API_KEY environment variable |
| Langfuse US | LLM observability and manual evaluation | Project keys plus https://us.cloud.langfuse.com |
| product_catalog.csv | Product truth source | Raw content provided to prompt and Catalog Guard |
| crm_export_sample.csv | Weekly summary source | Parsed by Weekly Sales Aggregator |


# 12. Release Plan

1. Package exported Langflow flows, prompts, custom components, sample data, evaluation results, evidence, BRD, PRD, and README in GitHub.
1. Re-run T1-T11 after any prompt, schema, catalog, model, or guard change.
1. Conduct a controlled pilot with 3-5 representatives and human review of every draft.
1. Add production Gmail/CRM integrations only after OAuth, audit, retry, and approval-gate design review.
1. Expand to 20 representatives after two stable review cycles and acceptance of privacy, quality, and cost metrics.

# 13. Future Enhancements

- Human-in-the-loop approval component before sending email.
- OAuth-based Gmail ingestion and draft creation.
- CRM API integration with idempotency and duplicate detection.
- Automated Langfuse evaluators and dataset experiments.
- Catalog retrieval/indexing for larger inventories.
- Scheduled weekly execution, alerts, role-based access, and production retention policies.
