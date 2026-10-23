from google.cloud import firestore
from typing import Dict, Any
from document_models import NormalizedExpense
from document_client import load_config

def persist_expense_record(normalized_expense_data: Dict[str, Any]) -> Dict[str, Any]:
    config = load_config()
    project_id = config.get("google_project_id")
    collection_name = config.get("google_firestore_collection")

    if not all([project_id, collection_name]):
        raise ValueError("Google Cloud project ID or Firestore collection name is not configured.")

    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Google Cloud Firestore.")

    db = firestore.Client(project=project_id)
    
    normalized_expense = NormalizedExpense(**normalized_expense_data["normalized_expense"])

    # Convert Pydantic model to dictionary for Firestore
    expense_record_dict = normalized_expense.dict()
    
    # Add a document to the collection
    doc_ref = db.collection(collection_name).add(expense_record_dict)
    
    return {"status": "success", "document_id": doc_ref[1].id}
