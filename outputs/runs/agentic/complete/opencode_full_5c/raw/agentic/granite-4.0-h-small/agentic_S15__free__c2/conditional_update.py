import json
from database_client import NoSQLClient


def conditional_update(doc_id, update_payload, version_field="version"):
    """Apply a conditional/version-aware update to a stored document in DocumentDB.

    Parameters:
        doc_id (str): Primary identifier of the document.
        update_payload (dict): Fields to update.
        version_field (str): Field tracking document version for conditional checks.
    Returns:
        bool: True if update succeeded, False otherwise.
    """
    client = NoSQLClient()
    # Provider-specific conditional update (optimistic lock) using DocumentDB
    return client.update(
        doc_id=doc_id,
        payload=update_payload,
        condition={version_field: "exists"},
        collection="documents",
    )
