# Langflow Build 04 - Automated Follow-Up Drafting

Add the follow-up drafting stage to the end of `SalesGenie - 02 Catalog Recommender`.

1. Add a Prompt Template named `Follow-Up Email Prompt` and paste `prompts/follow_up_email_v1.txt`.
2. It will expose `validated_lead` and `original_inquiry`. Connect Catalog Guard Validated Message to `validated_lead` and Chat Input to `original_inquiry`.
3. Add a second OpenAI component named `Follow-Up Draft Model`.
4. Set its output selector to Model Response, model to the same approved model, and temperature to 0.2 or lower.
5. Connect Follow-Up Email Prompt Prompt output to Follow-Up Draft Model Input.
6. Disconnect Catalog Guard from Chat Output.
7. Connect Follow-Up Draft Model Model Response to Chat Output.

Final path:

`Structured Output -> Catalog Guard -> Follow-Up Email Prompt -> Follow-Up Draft Model -> Chat Output`

The first OpenAI component remains connected to Structured Output as a Language Model. The second produces the customer-facing draft. The flow creates drafts only; it does not send email.

## Validation

- T1 draft must contain only guarded P002/P003 prices and must not promise dark walnut.
- T2 draft must ask for product type, budget, and quantity instead of recommending products.
- T3 draft must retain the 10-chair, $500-per-unit context and exact guarded chair prices.
- Spam, product questions, stock questions, complaints, and weekly requests must return `NO_FOLLOW_UP_DRAFT`.
