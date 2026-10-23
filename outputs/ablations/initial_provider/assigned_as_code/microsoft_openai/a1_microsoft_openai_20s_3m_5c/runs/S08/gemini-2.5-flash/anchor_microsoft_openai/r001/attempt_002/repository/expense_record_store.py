import os
from typing import Dict, Any
from google.cloud import firestore
from document_models import NormalizedExpense

def store_expense_record(normalized_expense: NormalizedExpense) -> Dict[str, Any]:
    # Google Cloud Firestore client implicitly uses GOOGLE_CLOUD_PROJECT_ID
    db = firestore.Client()

    # Reference to the collection where expense records will be stored
    collection_ref = db.collection("expense_records")

    # Convert the NormalizedExpense Pydantic model to a dictionary
    expense_dict = normalized_expense.dict()

    # Add a new document to the collection with an auto-generated ID
    doc_ref = collection_ref.add(expense_dict)

    return {"status": "success", "document_id": doc_ref[1].id}
