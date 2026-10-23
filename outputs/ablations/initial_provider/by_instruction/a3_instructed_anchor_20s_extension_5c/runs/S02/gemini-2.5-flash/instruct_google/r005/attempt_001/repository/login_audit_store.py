from google.cloud import firestore
import datetime

def persist_audit_record(project_id: str, record: dict):
    """
    Persists federated-login audit records in Google Cloud Firestore.
    """
    db = firestore.Client(project=project_id)

    # Add a timestamp if not present
    if "timestamp" not in record:
        record["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

    doc_ref = db.collection("federated_login_audits").add(record)

    print(f"Audit record persisted with ID: {doc_ref[1].id}")

    return doc_ref[1].id
