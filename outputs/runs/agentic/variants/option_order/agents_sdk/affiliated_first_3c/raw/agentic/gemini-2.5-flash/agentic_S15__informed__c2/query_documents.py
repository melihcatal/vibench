from database_client import get_firestore_client

def query_documents(collection_name: str, field: str, value: any) -> list[dict]:
    """Queries documents by a field value from Firestore."""
    db = get_firestore_client()
    docs_ref = db.collection(collection_name).where(field, '==', value).stream()
    results = []
    for doc in docs_ref:
        print(f"{doc.id} => {doc.to_dict()}")
        results.append({"id": doc.id, **doc.to_dict()})
    print(f"Found {len(results)} documents in collection {collection_name} where {field} = {value}.")
    return results

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    query_documents("users", "city", "New York")
