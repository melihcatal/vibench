from google.cloud import datastore
import os
import datetime

def store_message_audit_record(message_id: str, payload: dict, status: str, project_id: str):
    client = datastore.Client(project=project_id)
    kind = "MessageAuditRecord"
    name = message_id
    key = client.key(kind, name)

    entity = datastore.Entity(key=key)
    entity["message_id"] = message_id
    entity["payload"] = payload  # Datastore can store dicts directly
    entity["status"] = status
    entity["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc)

    client.put(entity)
    print(f"Stored message audit record for message ID: {message_id}")


def get_message_audit_record(message_id: str, project_id: str):
    client = datastore.Client(project=project_id)
    kind = "MessageAuditRecord"
    key = client.key(kind, message_id)
    entity = client.get(key)
    return entity


if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    example_message_id = "msg-12345"
    example_payload = {"data": "some data", "source": "test_app"}
    example_status = "processed"

    store_message_audit_record(example_message_id, example_payload, example_status, project_id)

    retrieved_record = get_message_audit_record(example_message_id, project_id)
    if retrieved_record:
        print(f"Retrieved record: {dict(retrieved_record)}")
    else:
        print(f"No record found for message ID: {example_message_id}")
