import os
import datetime
from google.cloud import firestore


def persist_audit_record(record: dict) -> dict:
    # Initialize Firestore DB client
    db = firestore.Client()

    # Reference to the 'audit_records' collection
    collection_ref = db.collection('federated_login_audit_records')

    # Add a timestamp to the record
    record['timestamp'] = datetime.datetime.now(datetime.timezone.utc)

    # Add the record to the collection
    try:
        doc_ref = collection_ref.add(record)
        return {"status": "success", "document_id": doc_ref[1].id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
