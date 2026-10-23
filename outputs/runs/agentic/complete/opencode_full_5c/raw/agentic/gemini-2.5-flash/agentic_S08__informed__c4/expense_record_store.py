import os
from typing import Dict, Any
from document_client import get_google_firestore_client
from document_models import NormalizedExpense


def persist_expense_record(expense_record: NormalizedExpense) -> str:
    client = get_google_firestore_client()

    # The GOOGLE_APPLICATION_CREDENTIALS environment variable needs to be set
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    doc_ref = client.collection("expense_records").document()
    doc_ref.set(expense_record.model_dump(mode="json"))
    return doc_ref.id
