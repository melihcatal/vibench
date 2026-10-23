from google.cloud import firestore
from identity_models import LoginAuditRecord

def store_login_audit_record(record: LoginAuditRecord):
    db = firestore.Client()
    doc_ref = db.collection("login_audits").document()
    doc_ref.set(record.dict())