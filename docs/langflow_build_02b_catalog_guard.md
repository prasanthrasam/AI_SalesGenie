# Langflow Build 02b - Deterministic Catalog Guard

The prompt-only recommender repeatedly included an over-budget product and transferred a finish between catalog rows. Add a custom component after Structured Output to enforce price, availability, and same-row catalog grounding in code.

1. Add `New Custom Component` to the canvas.
2. Open its Code editor and replace the sample with `langflow/catalog_guard_component.py`.
3. Save/build it; it should appear as `Catalog Guard` with Structured Result and Raw Catalog CSV inputs.
4. Disconnect Structured Output from the final Stringify Parser.
5. Connect Structured Output directly to Catalog Guard -> Structured Result.
6. Change Read File's output selector from Structured Content to Raw Content. Connect Raw Content directly to both Prompt Template -> catalog_context and Catalog Guard -> Raw Catalog CSV. Catalog Stringifier is no longer needed.
7. Connect Catalog Guard -> Validated Message directly to Chat Output. The old final Parser is no longer needed.

The guard accepts raw CSV text directly, rejects product IDs absent from the catalog, products over the applicable budget, and products not marked In Stock. It reconstructs names, prices, availability, rationales, and response text using the actual catalog rows.
