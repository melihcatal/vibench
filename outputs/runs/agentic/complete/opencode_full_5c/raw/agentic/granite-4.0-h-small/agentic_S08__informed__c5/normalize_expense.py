from document_models import NormalizedExpense


class NormalizeExpense:
    def normalize(self, raw_fields):
        # Map raw extraction results to a standard JSON schema
        normalized = {
            "vendor": raw_fields.get("vendor"),
            "date": raw_fields.get("date"),
            "total": raw_fields.get("total"),
            "line_items": [
                {
                    "description": item["description"],
                    "quantity": item["quantity"],
                    "unit_price": item["unit_price"],
                    "total": item["total"],
                }
                for item in raw_fields.get("line_items", [])
            ],
        }
        return NormalizedExpense(**normalized)
