import os
from google.cloud import datastore
from messaging_models import EventMessage

# Configuration
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or that the environment has appropriate Google Cloud authentication.
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
AUDIT_KIND = "MessageAuditRecord"

def persist_message_record(event_message: EventMessage, processing_status: str, audit_data: dict | None = None) -> str:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = datastore.Client(project=PROJECT_ID)

    # Create a new entity for the audit record
    key = client.key(AUDIT_KIND)
    entity = datastore.Entity(key=key)

    # Populate the entity with message details and audit information
    entity["event_id"] = event_message.event_id
    entity["event_type"] = event_message.event_type
    entity["source"] = event_message.source
    entity["timestamp"] = event_message.timestamp
    entity["processing_status"] = processing_status # e.g., 'processed', 'failed', 'translated'
    entity["message_payload"] = event_message.to_json() # Store original payload as string
    if audit_data:
        entity.update(audit_data) # Add any additional audit data (e.g., moderation results, translation results)

    try:
        client.put(entity)
        print(f"Audit record for event ID {event_message.event_id} persisted with status: {processing_status}")
        return entity.key.id_or_name
    except Exception as e:
        print(f"Error persisting audit record for event ID {event_message.event_id}: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    # Example usage with a dummy EventMessage
    from datetime import datetime
    sample_event = EventMessage(
        event_id="audit-123",
        event_type="order.processed",
        data={
            "order_id": "ORD-987",
            "customer_email": "test@example.com",
            "total_amount": 99.99,
            "status": "completed"
        },
        source="order_processing_service",
        timestamp=datetime.utcnow().isoformat()
    )

    print("\n--- Persisting Audit Record ---")
    record_id = persist_message_record(sample_event, "completed", {"processor_version": "1.0", "processing_time_ms": 150})
    print(f"Persisted record with ID: {record_id}")

    sample_failed_event = EventMessage(
        event_id="audit-456",
        event_type="payment.failed",
        data={
            "transaction_id": "TXN-321",
            "amount": 50.00,
            "reason": "insufficient_funds"
        },
        source="payment_gateway",
        timestamp=datetime.utcnow().isoformat()
    )

    print("\n--- Persisting Failed Audit Record ---")
    record_id_failed = persist_message_record(sample_failed_event, "failed", {"error_code": "PAY-001", "retry_attempt": 3})
    print(f"Persisted record with ID: {record_id_failed}")
