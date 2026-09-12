# Langflow Build 02 - Inquiry Processing Workflow

## Goal

Process one inbound message end to end in a single operational flow. The flow classifies the message, extracts lead fields, recommends products from the approved catalog, validates all catalog claims deterministically, and drafts a follow-up email for human review.

Routing and extraction are embedded in this workflow, so no separate preliminary flow is required.

## Canvas

Import `langflow/02_catalog_recommender_followup.json`, or create a blank flow named `SalesGenie - 02 Catalog Recommender + Follow-Up` and add:

1. `Chat Input`
2. `Read File`
3. `Prompt Template`
4. OpenAI chat-model component
5. `Structured Output`
6. `Catalog Guard` custom component
7. Follow-up `Prompt Template`
8. Follow-up OpenAI model
9. `Chat Output`

## Connections

Upload `data/input/product_catalog.csv` into Read File with Advanced Parser disabled. Paste `prompts/catalog_recommender_v1.txt` into the first Prompt Template. This prompt contains the routing, extraction, qualification, and grounded recommendation rules. It creates two variables:

- `inbound_message`: connect from Chat Input
- `catalog_context`: connect from Read File Raw Content

Connect the first prompt to Structured Output Input Message. Connect the first OpenAI model's `Language Model` output to Structured Output and set temperature to 0. Connect Structured Output, Read File Raw Content, and Chat Input to Catalog Guard as described in `docs/langflow_build_02b_catalog_guard.md`.

Connect Catalog Guard's validated message and the original Chat Input to the follow-up Prompt Template. Connect that prompt to the follow-up OpenAI model, then connect the model response to Chat Output. The final output remains a draft and must not be sent automatically.

## Schema additions

Create the routing and extraction rows from `prompts/router_extractor_langflow_table.csv`, then add the rows in `prompts/catalog_recommender_schema_additions.csv`. Use parallel typed lists rather than a list of dictionaries because this is more reliably validated by the Structured Output component.

## First checks

- T1 must recommend only in-stock standing desks at or below $800 and must not claim a dark-walnut finish unless the catalog says so.
- T2 must return no recommendations and request missing details.
- T4 must answer that the Oak Executive Desk is available in Natural Oak and Dark Walnut, without classifying it as a lead.
- T10 must state that the Walnut Executive Desk is out of stock and must not invent a restock date.
