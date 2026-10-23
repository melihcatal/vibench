from google.cloud import firestore
import os
from .identity_models import AuditEvent, asdict


def persist_federated_login_audit(event: AuditEvent) -> str:
    db = firestore.Client()
    _, doc_ref = db.collection("federated_login_audits").add(asdict(event))
    return doc_ref.id
