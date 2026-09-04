# Langflow Build 03 - Weekly Summary

Create a blank flow named `SalesGenie - 03 Weekly Summary`.

1. Add Read File and upload `data/input/crm_export_sample.csv`.
2. Change Read File output to Raw Content.
3. Add New Custom Component and replace its code with `langflow/weekly_aggregator_component.py`.
4. Connect Read File Raw Content -> Weekly Sales Aggregator Raw CRM CSV.
5. Connect Weekly Summary -> Chat Output.
6. Run the flow and retain the output as T11 evidence.

Expected sample metrics:

- Total leads: 7
- Hot: 4, Warm: 2, Cold: 1
- Average known budget: $18,960 across 5 numeric budgets
- Missing budgets: 2
- Top normalized categories: Desk and Full Office Package, 2 each

The result includes all source lead IDs so the report is traceable to processed data.

