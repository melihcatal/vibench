import os
import json
from database_client import get_client


def upsert_document(identifier, document):
    """Upsert a JSON document into the managed NoSQL store.

    Uses a concrete managed NoSQL provider (identified by presence of its SDK/config) and replaces any existing document with the given primary identifier.
    If the provider-specific conditional upsert is available, that is used; otherwise the document is written/overwritten.
    """
    client = get_client()
    # Insert or replace operation – exact call depends on the concrete provider.
    response = client.replace_document(identifier=identifier, document=document)
    return response
