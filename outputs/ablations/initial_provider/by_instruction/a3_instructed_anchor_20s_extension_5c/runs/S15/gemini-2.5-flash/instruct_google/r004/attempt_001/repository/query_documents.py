from database_client import get_firestore_client

def query_documents(collection_name: str, field_name: str, field_value: any) -> list[dict]:
    """Queries documents in a Google Cloud Firestore collection by a field value.

    Args:
        collection_name (str): The name of the Firestore collection.
        field_name (str): The name of the field to query by.
        field_value (any): The value of the field to match.

    Returns:
        list[dict]: A list of matching documents.
    """
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()

    results = []
    for doc in docs:
        results.append({**doc.to_dict(), "id": doc.id})
    
    print(f"Found {len(results)} documents matching query in collection {collection_name}.")
    return results
