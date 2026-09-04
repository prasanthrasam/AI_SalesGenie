# Extended Capability Evaluation

## Automated Follow-Up Drafting

Selected extended capability: personalized response email drafts with recommended products and pricing.

### Cold lead test

- Input: `Hi, I need furniture.`
- Result: Pass
- Evidence: Generic greeting, no invented products, requested furniture type, budget, and quantity, and included a clear reply request.

### Grounded recommendation test

- Input: standing desk under $800 with a dark-walnut preference
- Result: Pass
- Included only validated P002 at $749 and P003 at $449.
- Excluded P004 because its $899 price exceeded the budget.
- Did not claim that P002 or P003 has a dark-walnut finish.
- Explicitly stated that the catalog does not confirm dark walnut and asked whether the customer is flexible.
- Included a clear next step and standard sales-team signature.

### Safety behavior

- The workflow creates a draft only and does not send customer email automatically.
- Non-sales routes are instructed to return `NO_FOLLOW_UP_DRAFT`.
- Product facts come from Catalog Guard's validated result; the original inquiry is used only for customer-stated requirements.

