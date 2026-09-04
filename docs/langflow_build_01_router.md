# Langflow Build 01 - Router and Lead Extractor

## Goal

Turn one inbound email into validated structured JSON and create the first observable Langfuse trace.

## Canvas

Create a blank flow named `SalesGenie - 01 Router and Extractor`.

Add and connect these components, using the closest available names in your Langflow version:

1. `Chat Input`
2. `Prompt Template`
3. Your chat-model component
4. `Structured Output`
5. `Parser`
6. `Chat Output`

Configure the model node with credentials and change its bottom output selector from `Model Response` to `Language Model`. Connect that output to the Structured Output node's `Language Model` input.

Paste the complete contents of `prompts/router_extractor_v1.txt` into Prompt Template. Langflow will expose an `inbound_message` input. Connect Chat Input to that prompt variable, then connect Prompt Template's Prompt output to Structured Output's Input Message. This ensures the routing rules reach the Structured Output component even in versions that do not expose Format Instructions.

Click `Open table` under Output Schema and create the rows from `prompts/router_extractor_langflow_table.csv`. Langflow's table supports `str`, `int`, `float`, `bool`, and `dict`, plus an `As List` switch.

Connect Structured Output to a `Parser`, then connect the Parser's Message output to `Chat Output`. In the Parser template, include the fields you want displayed; for the first run, displaying the complete structured record is acceptable.

Set temperature to `0` or the lowest supported value. Do not rely on the model node's System Message when it emits a Language Model object; some versions don't propagate that text into Structured Output. Do not add memory, tools, or catalog retrieval in this first flow.

## First validation inputs

Run these before adding more components:

### Detailed inquiry

`I need a standing desk under $800 for my home office, dark walnut finish. Email: john@corp.com`

Expected: `sales_inquiry`, Hot or Warm, budget_total 800, email present, no invented customer name.

### Product question

`What colors does the oak desk come in?`

Expected: `product_question`, lead_tier null.

### Spam

`asdfjkl; spam spam buy now click here!!!`

Expected: `spam`, lead_tier null.

## Langfuse check

Configure Langflow's Langfuse environment variables outside the canvas. After restarting Langflow, run the three tests and verify that each execution appears as a separate trace. Never store Langfuse or model API secrets in exported flow JSON.

## Evidence to retain

- Canvas screenshot
- One structured output screenshot
- Langfuse trace screenshot
- Exported flow JSON saved as `langflow/01_router_extractor.json`
