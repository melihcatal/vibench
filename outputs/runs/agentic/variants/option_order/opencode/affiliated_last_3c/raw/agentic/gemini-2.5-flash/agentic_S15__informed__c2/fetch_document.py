from database_client import db


def fetch_document(document_id: str):
    doc_ref = db.collection("documents").document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "document": doc.to_dict()}
    else:
        return {"status": "not_found", "document_id": document_id}
