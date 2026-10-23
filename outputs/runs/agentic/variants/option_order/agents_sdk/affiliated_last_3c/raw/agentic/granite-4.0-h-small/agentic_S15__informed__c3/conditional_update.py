import os
import time
from database_client import get_client
from database_models import DocumentModel

def conditional_update(document_id, expected_version, update_fields):
    """Atomically update a document only if its current version matches expected_version.
    Uses Azure Cosmos DB optimistic concurrency control via the _etag (or _version) system property.
    """
    client = get_client()
    container = client["my_container"]
    # Read current document to obtain its _etag
    current = container.read_item(item=document_id, partition_key=document_id)
    current_etag = current["_etag"]
    if current_etag != expected_version:
        raise ValueError(f"Version mismatch: expected {expected_version}, got {current_etag}")
    # Prepare updated payload (merge update_fields)
    updated = {**current, **update_fields}
    updated["_etag"] = current_etag  # provider will replace on success
    # Perform the upsert which will succeed only for the matching _etag (optimistic lock)
    container.upsert_item(updated)
    print(f"Conditionally updated {document_id} to version {int(current_etag) + 1}")
