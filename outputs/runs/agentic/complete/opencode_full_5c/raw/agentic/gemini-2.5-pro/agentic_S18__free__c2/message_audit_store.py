import os
from datetime import datetime
from google.cloud import datastore
from messaging_models import ProcessingResult


def store_audit_record(project_id: str, result: ProcessingResult):
    client = datastore.Client(project=project_id)

    kind = "MessageAudit"
    name = result.message_id
    key = client.key(kind, name)

    entity = datastore.Entity(key=key)
    entity.update(
        {
            "processed_at": datetime.utcnow(),
            "status": result.status,
            "error_message": result.error_message,
            "message_id": result.message_id,
        }
    )

    client.put(entity)

    print(f"Stored audit record for message {result.message_id} in Datastore.")
    return key


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    audit_result = ProcessingResult(message_id="audit-msg-789", status="success")

    store_audit_record(gcp_project_id, audit_result)

    failed_audit_result = ProcessingResult(
        message_id="audit-msg-456",
        status="failed",
        error_message="Connection timed out",
    )
    store_audit_record(gcp_project_id, failed_audit_result)
