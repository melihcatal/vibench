from database_client import db


def fetch_document(document_id):
    doc_ref = db.collection("documents").document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
