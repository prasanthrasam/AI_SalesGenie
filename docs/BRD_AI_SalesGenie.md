# Business Requirements Document

## AI SalesGenie

AI-powered sales qualification, catalog recommendation, follow-up drafting, and weekly insights

| Organization | Oak & Ember Interiors |
| --- | --- |
| Document owner | AI Product / Technical Program Management |
| Version | 1.0 |
| Date | September 4, 2026 |
| Status | Final capstone submission |


# 1. Executive Summary

Oak & Ember Interiors needs to reduce manual effort and inconsistency in inbound sales processing. AI SalesGenie is a Langflow-based assistant that extracts inquiry details, routes message types, qualifies valid leads, recommends products using the supplied catalog, drafts grounded follow-up emails, and produces weekly sales summaries. Langfuse provides trace-level evidence for quality, latency, token usage, cost, and human evaluation.


# 2. Business Context and Problem

- Sales representatives spend approximately 2-3 hours per day reading and interpreting inbound inquiries.
- Manual spreadsheet entry creates omissions, duplicates, and inconsistent records.
- Manual product matching is slow and can violate budget or availability constraints.
- Lead qualification is inconsistent because Hot, Warm, and Cold criteria are not standardized.
- CRM visibility is delayed, and weekly reporting consumes up to half a day each Friday.

# 3. Business Objectives

| Objective | Desired outcome | Primary measure |
| --- | --- | --- |
| Accelerate lead handling | Automate extraction, routing, and qualification | Median handling time per inquiry |
| Improve recommendation quality | Use only catalog-grounded products, prices, features, and availability | Catalog-grounding and hallucination rate |
| Increase sales consistency | Apply repeatable lead-tier and budget rules | Routing and qualification accuracy |
| Improve customer response | Produce personalized, review-ready email drafts | Draft acceptance and response time |
| Improve management visibility | Generate traceable weekly sales summaries | Report preparation time and reconciliation accuracy |


# 4. Stakeholders and Benefits

| Stakeholder | Decision / responsibility | Expected benefit |
| --- | --- | --- |
| CTO and Software Development leadership | Technology strategy, security, platform governance | Reusable agent platform with measurable reliability and cost |
| VP/Head of Sales | Sales process ownership and rollout approval | Faster response, consistent qualification, improved pipeline visibility |
| Sales representatives | Review and act on qualified leads and drafts | Less administrative work and faster customer engagement |
| Sales operations / CRM administrators | Data quality, taxonomy, reporting | Structured records and fewer omissions |
| Product and inventory teams | Catalog and availability accuracy | Recommendations tied to the approved catalog |
| Customers | Provide requirements and receive responses | Faster, relevant, transparent recommendations |
| AI PM/TPM | Requirements, evaluation, rollout, governance | Traceable acceptance criteria and operational metrics |


# 5. Scope


## 5.1 In scope

- Process text-based customer inquiries and extract identity, product interest, budget, quantity, urgency, deadline, and requirements.
- Route sales inquiries, product questions, stock questions, competitor comparisons, complaints, spam, and weekly-summary requests.
- Classify valid sales leads as Hot, Warm, or Cold.
- Recommend one to three in-stock catalog products under applicable total or per-unit budgets.
- Apply deterministic catalog validation before customer-facing drafting.
- Draft personalized follow-up emails using validated products and exact prices.
- Aggregate CRM sample data into weekly lead-tier, category, and budget insights.
- Trace execution and record model, token, cost, latency, input/output, and human scores in Langfuse.

## 5.2 Out of scope for this release

- Automatically sending email or modifying a production CRM without human review.
- Real-time inventory reservation, payment processing, or order placement.
- Claims about competitor products that are not present in approved data.
- Fine-tuning, multilingual support, image-based product search, and production-scale identity management.

# 6. Business Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| BR-01 | The solution shall reduce manual interpretation by extracting structured fields from inbound inquiry text. | High |
| BR-02 | The solution shall distinguish valid sales leads from product questions, stock questions, complaints, spam, and reporting requests. | High |
| BR-03 | The solution shall assign Hot, Warm, or Cold only to valid sales inquiries using consistent criteria. | High |
| BR-04 | The solution shall recommend only products present in the approved catalog and respect budget and availability constraints. | Critical |
| BR-05 | The solution shall not transfer a feature, finish, price, or availability claim between catalog rows. | Critical |
| BR-06 | The solution shall ask for missing information when a request is too vague for a safe recommendation. | High |
| BR-07 | The solution shall draft a customer-ready follow-up email without automatically sending it. | Medium |
| BR-08 | The solution shall produce a weekly summary traceable to actual CRM records. | High |
| BR-09 | The solution shall provide observability for quality, latency, token usage, cost, and failures. | High |
| BR-10 | The solution shall avoid storing API secrets in exported flows or source control. | Critical |


# 7. Business Rules

- A recommendation must match the requested product category and be in stock unless the user explicitly asks only for stock information.
- When quantity and total budget are known, the effective per-unit limit is total budget divided by quantity.
- Out-of-stock products cannot be described as available, and missing restock dates cannot be invented.
- Product questions do not receive Hot, Warm, or Cold lead tiers.
- Spam produces no recommendation and no sales action.
- Competitor differentiation may describe Oak & Ember catalog facts but may not invent competitor facts.
- If requested requirements are not confirmed by the catalog, the response must disclose the limitation and request flexibility.

# 8. Success Metrics

| Metric | Definition | Initial target |
| --- | --- | --- |
| Baseline pass rate | Passed cases across mandatory T1-T11 dataset | 11/11 required checks |
| Routing accuracy | Correct route divided by evaluated inquiries | >= 95% before pilot |
| Catalog grounding | Recommendations supported by an exact catalog row | 100% |
| Budget compliance | Recommendations at or below the applicable budget | 100% |
| Hallucination count | Unsupported product, price, availability, or feature claims | 0 critical claims |
| Operational efficiency | Time saved from manual lead processing | >= 50% during pilot |
| Draft acceptance | Drafts accepted with no or minor edits | >= 80% during pilot |


# 9. Assumptions, Dependencies, and Constraints

- The product catalog and CRM export are accurate, current, and authorized for use.
- OpenAI API availability and rate limits support the pilot workload.
- Langflow remains the workflow runtime and Langfuse remains the observability platform.
- Customer email is treated as sensitive data and trace access is restricted.
- The proof of concept uses file input rather than production Gmail and CRM APIs.
- A human remains accountable for reviewing drafts before external communication.

# 10. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Model invents or misattributes product facts | Customer misinformation | Deterministic Catalog Guard and exact-row reconstruction |
| Stale catalog or CRM data | Incorrect availability or reporting | Data ownership, timestamps, validation, and refresh controls |
| Sensitive data appears in traces | Privacy or compliance exposure | Synthetic testing, access controls, redaction, retention policy |
| Automated draft is sent without review | Brand or contractual risk | Draft-only workflow and future human approval gate |
| Model/API outage | Delayed processing | Visible failure state, retry policy, and manual fallback |
| Prompt or model changes regress quality | Inconsistent decisions | Versioned prompts, baseline regression suite, Langfuse scores |


# 11. Rollout and Governance

1. Pilot with 3-5 sales representatives using synthetic and low-risk inquiries.
1. Review trace quality weekly and resolve any hallucination, routing, or privacy issues.
1. Expand to 20 representatives after baseline, security, and operational acceptance gates pass.
1. Introduce production connectors only after OAuth, access control, audit, retention, and human-approval requirements are approved.
1. Monitor accuracy, cost per lead, latency, draft acceptance, and user feedback after rollout.

# 12. Acceptance Summary

Business acceptance requires all core workflows to run end to end, baseline tests T1-T11 to meet mandatory expectations, catalog and budget guardrails to pass, Langfuse evidence to be available, API secrets to remain outside exported artifacts, and the automated follow-up capability to remain draft-only.
