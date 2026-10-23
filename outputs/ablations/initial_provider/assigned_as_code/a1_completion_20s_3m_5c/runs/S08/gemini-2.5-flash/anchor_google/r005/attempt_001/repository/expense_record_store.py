import os
from typing import Dict, Any
from google.cloud import firestore
from document_models import ExpenseRecord


def persist_expense_record(expense_record: ExpenseRecord) -> Dict[str, Any]:
    # Initialize Firestore DB client
    project_id = os.getenv("GCP_PROJECT_ID")
    db = firestore.Client(project=project_id)

    # Reference to the collection where expense records will be stored
    collection_ref = db.collection("expense_records")

    # Convert the ExpenseRecord Pydantic model to a dictionary
    record_dict = expense_record.dict()

    # Add a new document to the collection
    # Firestore automatically generates a document ID if not provided
    doc_ref = collection_ref.add(record_dict)

    return {"status": "success",
            "document_id": doc_ref[1].id,
            "collection": "expense_records",
            "provider": "Google Cloud Firestore"}