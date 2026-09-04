import csv
import io
import json
from collections import Counter

from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Message


class WeeklyAggregatorComponent(Component):
    display_name = "Weekly Sales Aggregator"
    description = "Calculates traceable weekly lead metrics from CRM CSV data."
    icon = "ChartColumn"
    name = "WeeklyAggregatorComponent"

    inputs = [
        MessageTextInput(name="crm_csv", display_name="Raw CRM CSV", required=True),
    ]

    outputs = [
        Output(name="weekly_summary", display_name="Weekly Summary", method="build_summary")
    ]

    @staticmethod
    def normalize_category(product_interest: str) -> str:
        value = product_interest.lower()
        if "desk" in value:
            return "Desk"
        if "chair" in value:
            return "Chair"
        if "table" in value:
            return "Table"
        if "full office" in value:
            return "Full Office Package"
        if not value or value == "unknown":
            return "Unknown"
        return product_interest.strip()

    def build_summary(self) -> Message:
        source = self.crm_csv.text if hasattr(self.crm_csv, "text") else str(self.crm_csv)
        rows = list(csv.DictReader(io.StringIO(source)))
        if not rows:
            raise ValueError("No CRM rows were parsed")

        tier_counts = Counter((row.get("lead_tier") or "Unknown").strip() for row in rows)
        category_counts = Counter(
            self.normalize_category(row.get("product_interest") or "") for row in rows
        )

        known_budgets = []
        for row in rows:
            raw_budget = (row.get("budget") or "").strip()
            try:
                known_budgets.append(float(raw_budget))
            except ValueError:
                continue

        average_budget = sum(known_budgets) / len(known_budgets) if known_budgets else None
        top_count = max(category_counts.values()) if category_counts else 0
        top_categories = sorted(
            category for category, count in category_counts.items() if count == top_count
        )

        summary = {
            "total_leads": len(rows),
            "lead_tier_breakdown": {
                "Hot": tier_counts.get("Hot", 0),
                "Warm": tier_counts.get("Warm", 0),
                "Cold": tier_counts.get("Cold", 0),
            },
            "category_breakdown": dict(sorted(category_counts.items())),
            "top_categories": top_categories,
            "average_budget": round(average_budget, 2) if average_budget is not None else None,
            "known_budget_count": len(known_budgets),
            "missing_budget_count": len(rows) - len(known_budgets),
            "source_lead_ids": [row.get("lead_id", "") for row in rows],
        }
        return Message(text=json.dumps(summary, indent=2))

