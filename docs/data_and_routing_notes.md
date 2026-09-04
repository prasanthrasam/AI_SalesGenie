# Data and Routing Notes

## Supplied data

- 15 sample inquiry emails
- 20 catalog products across Desk, Chair, Table, Accessory, and Storage
- 7 sample CRM lead records
- 11 mandatory baseline evaluation inputs

## Required message routes

The message router must choose exactly one of:

- `sales_inquiry`
- `product_question`
- `stock_question`
- `complaint`
- `spam`
- `weekly_summary_request`

Only `sales_inquiry` continues to Hot/Warm/Cold lead qualification. Other routes must not receive a lead tier.

## Grounding constraints

- Recommend only product IDs present in `product_catalog.csv`.
- Copy price, features, finishes, and availability from the catalog.
- Do not infer restock dates, discounts, price matching, delivery dates, or competitor features.
- If required information is absent, ask for it explicitly.
- For bulk orders, compare the product price with the per-unit budget and preserve both total and per-unit budget.
- Weekly figures must be calculated from stored structured records, not estimated by the language model.

