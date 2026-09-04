# Langflow Build 02 - Catalog Recommender

## Connections

Upload `data/input/product_catalog.csv` into Read File with Advanced Parser disabled. Paste `prompts/catalog_recommender_v1.txt` into Prompt Template. This creates two variables:

- `inbound_message`: connect from Chat Input
- `catalog_context`: connect from Read File Raw Content

Connect Prompt to Structured Output Input Message. Keep OpenAI Language Model connected to Structured Output, temperature 0, and keep Structured Output -> Stringify Parser -> Chat Output.

## Schema additions

Retain the router/extractor fields and add the seven rows in `prompts/catalog_recommender_schema_additions.csv`. Use parallel typed lists rather than a list of dictionaries because this is more reliably validated by the Structured Output component.

## First checks

- T1 must recommend only in-stock standing desks at or below $800 and must not claim a dark-walnut finish unless the catalog says so.
- T2 must return no recommendations and request missing details.
- T4 must answer that the Oak Executive Desk is available in Natural Oak and Dark Walnut, without classifying it as a lead.
- T10 must state that the Walnut Executive Desk is out of stock and must not invent a restock date.
