import json
from database_client import NoSQLClient


def upsert_document(doc_id, document):
    """Upsert a JSON document by its primary identifier using Amazon DocumentDB.

    Parameters:
        doc_id (str): The primary identifier of the document.
        document (dict): The JSON document to upsert.
    """
    client = NoSQLClient()
    # Provider-specific upsert using DocumentDB API
    client.upsert(doc_id=doc_id, payload=document, collection="documents")
