import os
import json
from normalize_expense import NormalizeExpense
from document_client import DocumentClient
from validate_document_fields import ValidateDocumentFields

# Managed document store client (e.g., Azure Cosmos DB)
COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")


class ExpenseRecordStore:
    def __init__(self):
        self.client = DocumentClient(endpoint=COSMOS_ENDPOINT, key=COSMOS_KEY)

    def persist(self, expense: NormalizeExpense):
        if not ValidateDocumentFields.validate(expense):
            raise ValueError("Expense validation failed")
        # Serialize to JSON and store in Cosmos DB container
        document = {
            "id": expense.vendor.replace(" ", "-"),
            "vendor": expense.vendor,
            "date": expense.date,
            "total": expense.total,
            "line_items": expense.line_items,
            "extracted_at": datetime.utcnow().isoformat(),
        }
        # Placeholder for Cosmos DB write operation
        self.client.write_document(container="expenses", document=document)
        print(f"Persisted expense for {expense.vendor}")
