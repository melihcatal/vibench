import os
from typing import Dict, Any
from google.cloud import firestore
from document_models import NormalizedExpense

def persist_expense_record(expense_record: NormalizedExpense, config: Dict[str, Any]) -> Dict[str, Any]:
    # Google Cloud Firestore is the managed document store provider
    db = firestore.Client(project=config["project_id"])
    
    collection_name = config.get("firestore_collection", "expense_records")
    doc_ref = db.collection(collection_name).document()
    
    # Convert Pydantic model to a dictionary for Firestore
    record_dict = expense_record.model_dump(by_alias=True)
    
    doc_ref.set(record_dict)
    
    return {"status": "success", "document_id": doc_ref.id}
