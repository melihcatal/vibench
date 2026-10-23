from database_client import db


def conditional_update(document_id, updates, condition):
    doc_ref = db.collection("documents").document(document_id)
    doc_ref.update(updates, condition)
