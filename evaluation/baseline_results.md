# Baseline Evaluation Results

Record the actual results for T1-T11 after the workflow is operational. Do not mark a test as passed without retaining its output and Langfuse trace evidence.

| Test | Expected behavior | Actual result | Pass/Fail | Langfuse trace | Notes |
|---|---|---|---|---|---|
| T1 | Detailed standing-desk inquiry | Guard retained P002 ($749) and P003 ($449), removed P004 ($899), and rebuilt product facts from catalog | Pass | `2a3d1e25806c3f1bab8d009032bc87dd` | Grounded output, usage/cost, follow-up, and `overall_pass: True` evidence retained |
| T2 | Vague inquiry; request details | Returned Cold, no recommendations, and requested product type, budget, and quantity | Pass | Pending Langfuse setup | No invented customer or product details |
| T3 | Bulk chairs; per-unit budget and urgency | Returned Hot, quantity 10, $5,000 total/$500 unit, High urgency, and eligible P006/P007 recommendations | Pass - cleanup noted | Pending Langfuse setup | Name/company inferred from email domain; remove before final run |
| T4 | Product question; no lead tier | Returned `product_question`, empty tier, and exact P004 finishes: Natural Oak and Dark Walnut | Pass | Pending Langfuse setup | Response also used catalog material and dimensions |
| T5 | Grounded competitor positioning | Returned Warm sales inquiry, identified IKEA, and used exact P002/P003 catalog differentiators | Pass | Pending Langfuse setup | Accessory false match removed by category guard |
| T6 | Low-budget catalog handling | Returned Cold and recommended only in-stock P015 Desk Organizer Set at $39 | Pass | Pending Langfuse setup | No product above $50 included |
| T7 | Spam; no qualification or recommendation | Returned spam, empty tier and recommendations, and no sales action | Pass | `39f71fe4203031035fa45c82b7101c92` | No customer details invented; Catalog Guard evidence and `overall_pass: True` score retained |
| T8 | Conference-table inquiry with firm context | Returned Hot and grounded P011 12-person table at $2,499 with law-firm context | Pass - cleanup noted | Pending Langfuse setup | Clear generic `Law Firm` from customer_name before final run |
| T9 | Minimal inquiry; request details | Returned Cold sales inquiry, no recommendations, and requested type, budget, quantity, and requirements | Pass | Pending Langfuse setup | No invented details |
| T10 | Correct out-of-stock response | Returned stock_question and correctly reported P001 Out of Stock with no restock date available | Pass | Pending Langfuse setup | No false availability claim |
| T11 | Traceable weekly summary | Returned 7 leads; Hot 4, Warm 2, Cold 1; top categories Desk and Full Office Package; average known budget $18,960 | Pass | Pending Langfuse setup | Traceable to L001-L007; 5 known and 2 missing budgets |
