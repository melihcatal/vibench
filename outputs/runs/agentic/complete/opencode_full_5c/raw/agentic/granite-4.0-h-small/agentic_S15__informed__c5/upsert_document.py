import os
from database_client import ManagedNoSQLClient


def upsert_document(identifier, document):
    """Upsert a JSON document into the managed NoSQL store.

    Args:
        identifier (str): Primary key identifier for the document.
        document (dict): The JSON document payload.
    """
    client = ManagedNoSQLClient()
    # Use provider-specific upsert operation (e.g., replace or merge)
    client.upsert(identifier, document)
    print(f"Document {identifier} upserted successfully.")
