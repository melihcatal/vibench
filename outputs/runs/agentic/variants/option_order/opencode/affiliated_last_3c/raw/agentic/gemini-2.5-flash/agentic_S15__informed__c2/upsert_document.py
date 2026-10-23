from database_client import db


def upsert_document(document_id: str, data: dict):
    doc_ref = db.collection("documents").document(document_id)
    doc_ref.set(data)
    return {"status": "success", "document_id": document_id}
