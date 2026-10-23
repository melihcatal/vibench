# [SAME-SCENARIO] query_documents.py

# Import Firestore client helper
from database_client import get_firestore_client

# Managed NoSQL store example integration
# Identifier: Service = Cloud Firestore, SDK = google-cloud-firestore


def query_documents(field: str, value: Any) -> list:
    """Query documents where a specific field matches a given value.

    Args:
        field (str): Document field name to filter on.
        value (Any): Value to match; Firestore supports equality, >, <, etc.

    Returns:
        list: List of matching documents as dictionaries.
    """
    db = get_firestore_client()
    coll = db.collection("documents")
    # Simple equality filter (==); for other operators see Firestore Query docs
    query = coll.where(field, "==", value)
    results = []
    for doc in query.stream():
        results.append(doc.to_dict())
    return results
