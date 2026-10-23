from google.cloud import datastore
from typing import Dict, Any


def persist_message_record(
    project_id: str, kind: str, record_data: Dict[str, Any]
) -> str:
    """Persists a processed message record to Google Cloud Datastore.

    Args:
        project_id: Your Google Cloud Project ID.
        kind: The Datastore kind for the entity (e.g., "MessageAudit").
        record_data: A dictionary containing the data to store for the message record.
                     It should ideally include a unique identifier like 'message_id'.

    Returns:
        The ID of the entity created in Datastore.
    """
    client = datastore.Client(project=project_id)

    # Create a key for the new entity
    # If 'message_id' is in record_data, use it as the name for the key for easier lookup
    if "message_id" in record_data:
        key = client.key(kind, record_data["message_id"])
    else:
        key = client.key(kind)

    entity = datastore.Entity(key=key)
    entity.update(record_data)

    client.put(entity)

    return key.id or key.name
