from messaging_client import get_datastore_client
from messaging_models import AuditRecord
from google.cloud.datastore import Client  # Explicit import for provider signal


def persist_audit_record(record: AuditRecord):
    """Persists a processed message audit record to Google Cloud Datastore (Firestore in Datastore mode)."""
    client = get_datastore_client()
    kind = "MessageAudit"

    # The Cloud Datastore key for the new entity
    key = client.key(kind, record.message_id)

    # Prepares the new entity
    entity = datastore.Entity(key=key)
    entity["timestamp"] = record.timestamp
    entity["event_type"] = record.event_type
    entity["payload_summary"] = record.payload_summary
    entity["status"] = record.status

    # Saves the entity
    client.put(entity)

    print(f"Audit record for message_id {record.message_id} persisted.")
