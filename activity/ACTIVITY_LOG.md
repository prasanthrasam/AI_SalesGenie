# Activity Log

## 2026-09-01

- Reviewed the SalesGenie capstone problem statement and grading requirements.
- Selected Langflow for building agent workflows.
- Selected Langfuse for observability, tracing, and evaluation evidence.
- Defined a router followed by a sequential lead-processing pipeline.
- Chose automated follow-up drafting as the required extended capability.
- Confirmed that Langflow is installed and can be opened locally.
- Created this project workspace for all capstone artifacts and evidence.
- Imported the official ZIP resources: 15 inquiry emails, a 20-product catalog, a 7-row CRM sample, the T1-T11 evaluation inputs, and the reference problem statement.
- Validated the source schemas. The catalog contains product ID, category, price, description, availability, material, and dimensions; the CRM sample defines the target lead record fields.
- Identified routing cases beyond normal sales leads: product question, stock question, spam, and customer complaint.
- Authored router/extractor prompt v1 and a strict JSON schema for the routing stage later embedded in the inquiry workflow.
- Reviewed the initial Langflow canvas and corrected the design to use the model's Language Model output, Structured Output format instructions, an output-schema table, and a Parser before Chat Output.
- Ran routing checks. Spam passed, but the product question was incorrectly labeled `Inquiry`. Diagnosed that the model node's System Message was not reliably propagated to Structured Output and restored Prompt Template as the explicit carrier for routing rules.
- Retested T4 after routing rules were moved into Prompt Template. It correctly returned `product_question` with an empty lead tier; retained screenshot evidence and marked T4 passed pending Langfuse trace evidence.
- Validated the initial router/extractor prototype: six expected nodes, five edges, temperature 0, 11 schema rows, Stringify parser, and no raw OpenAI API key stored in the export.
- Extended the prototype into the operational catalog recommendation flow and added Read File. Authored grounded recommendation prompt v1, schema additions, connection instructions, and initial catalog validation checks.
- First catalog run reached Structured Output but returned `No structured output returned`. Simplified nested recommendation dictionaries into five aligned typed lists to improve schema reliability.
- First successful catalog-shaped T1 response failed grounding checks: it included P004 at $899 despite an $800 limit and falsely attributed a dark-walnut option to P002. It also incorrectly set `catalog_grounded` true. Strengthened hard-budget, same-row feature attribution, converter labeling, and pre-output validation rules.
- Retest after stronger prompt repeated the same T1 violations. Decided prompt-only enforcement was insufficient and authored a deterministic Catalog Guard custom component to validate product IDs, budget, availability, and rebuild product claims from exact catalog rows.
- Initial Catalog Guard run failed because it received a stringified Langflow table rather than raw CSV. Updated the component to accept the Read File DataFrame directly while retaining Catalog Stringifier only for prompt context.
- The installed Langflow Table raised a conversion error inside Catalog Guard. Simplified the design to use Read File Raw Content and pass original CSV text directly to the prompt and guard; Catalog Stringifier is no longer required.
- Catalog Guard passed T1's essential checks: retained P002/P003, rejected P004 because $899 exceeded the $800 budget, and rebuilt recommendation facts from exact catalog rows. Remaining cleanup: prevent name inference from email and remove the obsolete `default_value` schema field.
- Confirmed `default_value` was not a visible schema row; Langflow added it during table conversion. Updated Catalog Guard to remove the generated field from final output.
- First T2 run correctly returned no products and listed missing information but omitted the required Cold tier and used a generic fallback response. Updated Catalog Guard to enforce Cold for vague sales inquiries and construct a direct clarification request.
- T2 retest passed: Cold tier, empty recommendation lists, and a direct request for product type, budget, and quantity.
- T3 passed required bulk-order checks: Hot, quantity 10, $5,000 total and $500 per unit, High urgency, end-of-month deadline, and in-stock P006/P007 recommendations below the unit budget. Recorded improper name/company inference from the email domain as cleanup work.
- First catalog-flow T4 run routed correctly but Catalog Guard replaced the product answer with a generic no-match sales response. Updated the guard to receive the inbound message, locate explicitly named products, answer product/stock questions from exact catalog rows, route complaints/spam/weekly requests, clean formatted emails, and remove identities inferred only from email addresses.
- T4 retest passed: product-question route, empty lead tier, and exact catalog-grounded Natural Oak and Dark Walnut finishes for P004.
- First T5 run extracted IKEA but misrouted the comparison as a product question and produced no differentiators. Updated Catalog Guard to treat competitor comparisons with product interest as Warm sales inquiries and deterministically select matching in-stock standing desks when the model proposes none.
- T5 retest still failed because the model omitted product_interest despite explicit "standing desks" text. Updated the guard to use the original inbound message as a deterministic fallback for competitor routing and product matching.
- T5 routing then passed and produced grounded differentiators, but name matching also selected P013 Standing Desk Mat. Tightened deterministic matching to require category Desk, excluding accessories.
- T5 final retest passed with only P002/P003, Warm qualification, IKEA extraction, and catalog-grounded feature comparisons without competitor claims.
- T6 passed: Cold classification and a single grounded P015 recommendation at $39, with no product over the $50 budget.
- T7 passed: spam route, empty lead tier and recommendation lists, and explicit no-sales-action response.
- T8 passed required checks with Hot tier, $3,000 budget, law-firm context, and only P011 at $2,499. Recorded generic `Law Firm` appearing as customer_name as a cleanup issue.
- First T9 run returned product_question instead of Cold sales inquiry. Added deterministic handling for generic furniture requests without a question and cleanup for generic organization terms incorrectly placed in customer_name.
- T9 retest passed with Cold sales inquiry, empty recommendation lists, and direct requests for type, budget, quantity, and requirements.
- T10 passed with stock-question route, exact P001 Out of Stock status, empty tier, and no invented restock date.
- Authored a deterministic Weekly Sales Aggregator component and build guide for T11 using CRM CSV records, including tier/category breakdowns, known-budget average, missing-budget count, and source lead IDs.
- T11 weekly aggregation passed: 7 total leads; Hot 4, Warm 2, Cold 1; Desk and Full Office Package tied as top categories; average known budget $18,960 across 5 records; 2 missing budgets; source IDs L001-L007 retained for traceability.
- Authored the required extended capability: a grounded Follow-Up Drafting Agent prompt and Langflow build guide. It drafts personalized sales emails from validated recommendations and prices, asks clarifying questions for Cold leads, emits no draft for non-sales routes, and does not automatically send messages.
- Validated the Follow-Up Drafting Agent on a Cold lead: it produced a professional email asking for furniture type, budget, and quantity without inventing products or customer details.
- First T1 follow-up draft included correct products/prices but added unsupported marketing phrases (`premium choice`, `without compromising on quality`) and did not explicitly flag the unconfirmed dark-walnut preference. Tightened the prompt to prohibit embellishment, surface unsupported requirements, and avoid literal Markdown backslashes.
- Second T1 draft removed unsupported marketing claims but still did not name the unmet dark-walnut requirement because the structured record omitted it. Updated Follow-Up Email Prompt to receive the original inquiry separately for customer-stated requirements while retaining the validated record as the sole source of product facts.
- Corrected an unintended `customer_name` Prompt Template variable caused by braces in instructional text; the follow-up template now exposes only `validated_lead` and `original_inquiry`.
- Final T1 follow-up draft passed: exact P002/P003 prices and features, P004 excluded, dark-walnut availability explicitly unconfirmed, customer flexibility requested, and a clear next action included.
- Exported and validated the complete catalog-recommender/follow-up flow: 9 nodes, 11 edges, 22 structured fields, router and follow-up prompts embedded, Catalog Guard present, and no raw OpenAI API key stored.
- Exported and validated the weekly-summary flow: Read File, Weekly Sales Aggregator, and Chat Output connected by two edges; no raw API secret stored.
- Langfuse cloud authentication repeatedly redirected despite region and browser troubleshooting. Selected Langflow Native Traces as the open-source observability tool so trace evidence can be collected without an external account; documented metrics and evidence workflow.
- Captured the first instrumented follow-up trace. The Cold-lead draft passed, with Langfuse trace ID `096f5e6f3a4ea643f3a08dcd908e875f`, graph run ID `e582304c-ded2-4d52-a33c-4a96a93c872c`, and 3,063 input / 231 output tokens for the final drafting call. Estimated that call at approximately $0.00060; full-flow cost still requires the Structured Output span usage.
- Verified successful Langfuse ingestion in the US-region dashboard. The Tracing table now shows the complete SalesGenie run, including Prompt Template, Structured Output/model operations, Catalog Guard, Follow-Up Draft Model, and Chat Output observations.
- Saved five Langfuse evidence screenshots under `evaluation/evidence/langfuse` and added an index describing the tracing overview, router usage, Catalog Guard input/output, and follow-up model usage.
- Captured Langfuse trace `39f71fe4203031035fa45c82b7101c92` for T7. The deterministic guard returned `message_type: spam`, empty recommendation lists, and an explicit no-sales-action response.
- Created formal BRD and PRD deliverables in Word and GitHub-readable Markdown formats, updated the repository README with architecture and run instructions, and linked representative Langfuse trace `2a3d1e25806c3f1bab8d009032bc87dd` to T1.

## 2026-09-12

- Retired the standalone routing prototype because the operational catalog recommender and follow-up flow already contains the same behavior.
- Consolidated the repository around two operational flows: inquiry processing and weekly sales summary.
- Updated the README, build guide, workflow handout, presentation, and package references to match the two-flow architecture.

## Logging convention

For each work session, record:

- What changed
- Why the decision was made
- Test inputs used
- Results and trace references
- Problems found and next actions
