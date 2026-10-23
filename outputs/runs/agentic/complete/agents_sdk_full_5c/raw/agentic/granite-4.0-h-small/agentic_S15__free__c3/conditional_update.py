# conditional_update.py
# [SAME-SCENARIO] Perform a conditional/version-aware update on a document in Azure Cosmos DB (NoSQL)

import os
from database_client import get_cosmos_db_client
from database_models import ConditionalUpdatePayload

def conditional_update(document_id: str, update_data: dict, if_none_match: str = None) -> bool:
    """Update a document only if the provided version constraint matches.

    Uses Azure Cosmos DB's optimistic concurrency control via the If-None-Match header.
    Returns True if the update succeeded, False if precondition failed.
    """
    client = get_cosmos_db_client()
    container = client.get_container("mydb", "documents")
    item = container.read_item(item=document_id, partition_key=document_id)
    # Attach the version/Etag for conditional request
    if if_none_match:
        headers = {"If-Match": if_none_match}
    else:
        headers = {}
    # Merge update fields
    merged = {**item, **update_data}
    container.replace_item(item=document_id, body=merged, partition_key=document_id, **headers)
    return True  # replace raises exception on precondition failure, so we succeed if no exception
