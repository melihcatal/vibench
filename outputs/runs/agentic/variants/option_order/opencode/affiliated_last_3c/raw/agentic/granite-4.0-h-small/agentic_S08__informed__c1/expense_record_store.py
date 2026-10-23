import os
import json
from google.cloud import firestore


# Firestore client wrapper
class ExpenseStore:
    def __init__(self):
        # Uses default credentials configured via GOOGLE_APPLICATION_CREDENTIALS env var
        self.db = firestore.Client()
        self.collection = self.db.collection("expenses")

    def store(self, normalized: dict):
        doc_id = (
            normalized.get("merchant_or_vendor", "unknown")
            + "_"
            + normalized.get("date", "")
        )
        self.db.collection("expenses").document(doc_id).set(normalized)
        print(f"Stored expense record: {doc_id}")


if __name__ == "__main__":
    # Example usage with a normalized expense payload
    sample = {
        "merchant_or_vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": 123.45,
        "items": [
            {
                "description": "Widget A",
                "quantity": 2,
                "unit_price": 10.0,
                "total": 20.0,
            },
            {
                "description": "Widget B",
                "quantity": 1,
                "unit_price": 12.0,
                "total": 12.0,
            },
        ],
    }
    store = ExpenseStore()
    store.store(sample)
