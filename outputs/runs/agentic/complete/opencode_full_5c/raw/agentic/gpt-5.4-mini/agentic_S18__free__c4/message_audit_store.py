from google.cloud import firestore

from messaging_models import AuditRecord


def message_audit_store(
    message_id: str,
    status: str,
    payload,
    attributes,
    provider: str = "google-cloud-firestore",
):
    client = firestore.Client()
    record = AuditRecord(
        message_id=message_id,
        status=status,
        payload=payload or {},
        attributes=attributes or {},
        provider=provider,
    )
    client.collection("message_audit").document(message_id).set(record.__dict__)
    return {"stored": True, "message_id": message_id, "provider": provider}
