from database_client import db


def upsert_document(document_id, data):
    doc_ref = db.collection("documents").document(document_id)
    doc_ref.set(data)
