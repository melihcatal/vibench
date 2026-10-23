from google.cloud import firestore


def store_audit_record(record):
    db = firestore.Client()
    doc_ref = db.collection(u'audit_records').document()
    doc_ref.set(record)
