import os
from database_client import NoSQLClient
from database_models import Document

# Use Google Firestore as the managed NoSQL store
CLIENT = NoSQLClient(service='Firestore')

def query_documents(partition_key: str, field: str, value) -> list[dict]:
    """
    Query documents where `field` equals `value` within a partition identified by `partition_key`.
    
    Args:
        partition_key: The field used as a logical partition (can be the document ID or a parent collection ID).
        field: Field name to filter on.
        value: Exact value to match.
    Returns:
        List of document dicts matching the criteria.
    """
    col_ref = CLIENT.client.collection(partition_key)
    query = col_ref.where(field, '==', value)
    docs = [doc.to_dict() for doc in query.stream()]
    return docs
