import csv
import io
import re

from langflow.custom import Component
from langflow.io import DataInput, MessageTextInput, Output
from langflow.schema import Data, Message


class CatalogGuardComponent(Component):
    display_name = "Catalog Guard"
    description = "Deterministically validates recommendations against the product catalog and budget."
    icon = "ShieldCheck"
    name = "CatalogGuardComponent"

    inputs = [
        DataInput(name="result", display_name="Structured Result", required=True),
        MessageTextInput(name="catalog_text", display_name="Raw Catalog CSV", required=True),
        MessageTextInput(name="inbound_message", display_name="Inbound Message", required=True),
    ]

    outputs = [Output(name="validated_message", display_name="Validated Message", method="validate_result")]

    def validate_result(self) -> Message:
        payload = self.result.data if isinstance(self.result, Data) else self.result
        if not isinstance(payload, dict):
            raise ValueError("Structured Result must contain a JSON object")
        payload.pop("default_value", None)

        catalog_source = self.catalog_text.text if hasattr(self.catalog_text, "text") else str(self.catalog_text)
        rows = list(csv.DictReader(io.StringIO(catalog_source)))

        catalog = {row["product_id"].strip(): row for row in rows if row.get("product_id")}
        if not catalog:
            raise ValueError("No catalog rows were parsed")

        ids = payload.get("recommendation_product_ids") or []
        inbound = self.inbound_message.text if hasattr(self.inbound_message, "text") else str(self.inbound_message)
        inbound_without_emails = re.sub(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "", inbound)
        payload["email"] = str(payload.get("email") or "").replace("*", "").replace("\\", "")
        for identity_field in ("customer_name", "company"):
            candidate = str(payload.get(identity_field) or "").strip()
            if candidate and candidate.lower() not in inbound_without_emails.lower():
                payload[identity_field] = ""
        generic_name_terms = {"firm", "company", "procurement", "admin", "office", "customer"}
        customer_name = str(payload.get("customer_name") or "").strip()
        if customer_name and any(term in customer_name.lower().split() for term in generic_name_terms):
            payload["customer_name"] = ""
        total_budget = float(payload.get("budget_total") or 0)
        unit_budget = float(payload.get("budget_per_unit") or 0)
        quantity = int(payload.get("quantity") or 0)
        message_type = str(payload.get("message_type") or "").strip()
        product_interest = [str(x).strip().lower() for x in (payload.get("product_interest") or [])]
        competitor_mentions = payload.get("competitor_mentions") or []

        if message_type == "product_question" and "furniture" in inbound.lower() and "?" not in inbound:
            message_type = "sales_inquiry"
            payload["message_type"] = "sales_inquiry"

        competitor_has_product_context = bool(product_interest) or "standing desk" in inbound.lower()
        if competitor_mentions and competitor_has_product_context:
            message_type = "sales_inquiry"
            payload["message_type"] = "sales_inquiry"
            payload["lead_tier"] = "Warm"
            if not product_interest and "standing desk" in inbound.lower():
                product_interest = ["standing desks"]
                payload["product_interest"] = ["standing desks"]

        if not ids and competitor_mentions:
            interest_text = " ".join(product_interest) + " " + inbound.lower()
            if "standing desk" in interest_text:
                ids = [
                    row["product_id"]
                    for row in rows
                    if "standing desk" in row.get("product_name", "").lower()
                    and row.get("category", "").strip().lower() == "desk"
                    and row.get("availability", "").strip().lower() == "in stock"
                ][:3]

        if message_type != "sales_inquiry":
            payload["lead_tier"] = ""
        else:
            generic_interests = {"", "furniture", "something", "unknown"}
            has_specific_product = any(item not in generic_interests for item in product_interest)
            has_strong_signal = bool(total_budget > 0 or unit_budget > 0 or quantity > 0 or payload.get("deadline_text"))
            if competitor_mentions and has_specific_product:
                payload["lead_tier"] = "Warm"
            elif not has_specific_product:
                payload["lead_tier"] = "Cold"
            elif has_strong_signal:
                payload["lead_tier"] = payload.get("lead_tier") or "Hot"
            else:
                payload["lead_tier"] = payload.get("lead_tier") or "Warm"

        applicable_budget = unit_budget
        if applicable_budget <= 0 and total_budget > 0:
            applicable_budget = total_budget / quantity if quantity > 1 else total_budget

        accepted = []
        rejected = []
        for product_id in ids[:3]:
            row = catalog.get(str(product_id).strip())
            if row is None:
                rejected.append(f"{product_id}: not found in catalog")
                continue
            price = float(row["price"])
            if applicable_budget > 0 and price > applicable_budget:
                rejected.append(f"{product_id}: price {price:.2f} exceeds budget {applicable_budget:.2f}")
                continue
            if row.get("availability", "").strip().lower() != "in stock":
                rejected.append(f"{product_id}: {row.get('availability', 'availability unknown')}")
                continue
            accepted.append(row)

        payload["recommendation_product_ids"] = [r["product_id"] for r in accepted]
        payload["recommendation_product_names"] = [r["product_name"] for r in accepted]
        payload["recommendation_prices"] = [float(r["price"]) for r in accepted]
        payload["recommendation_availability"] = [r["availability"] for r in accepted]
        payload["recommendation_rationales"] = [
            f"{r['product_name']} costs ${float(r['price']):.2f} and is {r['availability'].lower()}. "
            f"Catalog description: {r['description']}"
            for r in accepted
        ]
        payload["catalog_grounded"] = True
        payload["guard_rejections"] = rejected

        mentioned_row = next(
            (row for row in rows if row.get("product_name", "").lower() in inbound.lower()),
            None,
        )

        if message_type == "product_question" and mentioned_row:
            payload["response_text"] = (
                f"Catalog information for {mentioned_row['product_name']}: {mentioned_row['description']} "
                f"Material: {mentioned_row['material']}. Dimensions: {mentioned_row['dimensions']}."
            )
        elif message_type == "stock_question" and mentioned_row:
            payload["response_text"] = (
                f"{mentioned_row['product_name']} is listed as {mentioned_row['availability']}. "
                "The catalog does not provide a restock date."
            )
        elif message_type == "complaint":
            payload["response_text"] = "This is a customer-service complaint and should be routed to a human support representative."
        elif message_type == "spam":
            payload["response_text"] = "Message identified as spam; no sales action taken."
        elif message_type == "weekly_summary_request":
            payload["response_text"] = "Weekly summary request detected; route to the weekly aggregation workflow."
        elif accepted:
            names = ", ".join(r["product_name"] for r in accepted)
            payload["response_text"] = (
                f"Catalog products that satisfy the hard price and availability checks: {names}. "
                "Any requested feature or finish must be confirmed in the individual catalog description."
            )
        elif message_type == "sales_inquiry" and not ids:
            missing = payload.get("missing_information") or ["product type", "budget", "requirements"]
            payload["response_text"] = "Please provide: " + ", ".join(str(item) for item in missing) + "."
        else:
            payload["response_text"] = (
                "No catalog product passed the hard price and availability checks. "
                "Ask the customer whether their requirements or budget are flexible."
            )

        import json
        return Message(text=json.dumps(payload, indent=2))
