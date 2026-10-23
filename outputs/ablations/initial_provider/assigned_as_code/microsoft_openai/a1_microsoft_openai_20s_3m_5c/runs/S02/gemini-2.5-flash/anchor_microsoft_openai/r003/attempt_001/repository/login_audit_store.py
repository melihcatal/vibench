import os
from google.cloud import firestore
from datetime import datetime

def store_login_audit_record(project_id: str, record: dict) -> dict:
    db = firestore.Client(project=project_id)
    collection_ref = db.collection("login_audit_records")
    
    # Add a timestamp if not already present
    if "timestamp" not in record:
        record["timestamp"] = datetime.utcnow()

    _, doc_ref = collection_ref.add(record)
    
    return {"status": "success", "document_id": doc_ref.id}

def get_login_audit_record(project_id: str, document_id: str) -> dict:
    db = firestore.Client(project=project_id)
    collection_ref = db.collection("login_audit_records")
    doc_ref = collection_ref.document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "data": doc.to_dict()}
    else:
        return {"status": "not_found", "message": f"Document with ID {document_id} not found."}
