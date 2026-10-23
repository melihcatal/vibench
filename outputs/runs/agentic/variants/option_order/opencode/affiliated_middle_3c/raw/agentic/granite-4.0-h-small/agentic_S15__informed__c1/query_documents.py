# SAME-SCENARIO
# query_documents.py - queries documents by a field value or partition-style key

# Provider: Google Firestore (managed NoSQL document store)
from google.cloud import firestore
from database_client import get_firestore_client


def query_documents(field: str, value) -> list:
    """Query Firestore documents that match a field value.

    Args:
        field (str): The field name to filter on.
        value: The value to match.

    Returns:
        list: A list of matching document data dictionaries.
    """
    db = get_firestore_client()
    query = db.collection("documents").where(field, "==", value)
    results = [doc.to_dict() for doc in query.stream()]
    return results
