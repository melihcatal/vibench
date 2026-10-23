from google.cloud import firestore
from database_client import get_firestore_client

def query_documents(collection_name: str, field_name: str, field_value: any) -> list[dict]:
    """Queries documents by a field value from Firestore."""
    db = get_firestore_client()
    docs = (
        db.collection(collection_name).where(field_name, "==", field_value).stream()
    )
    results = []
    for doc in docs:
        results.append({**doc.to_dict(), "id": doc.id})
    print(f"Queried {len(results)} documents from collection {collection_name}.")
    return results

if __name__ == '__main__':
    # Example usage (requires Firestore emulator or live project setup)
    # # Assuming some documents exist with a 'status' field
    # query_results = query_documents(
    #     collection_name="my_collection", field_name="status", field_value="active"
    # )
    # for doc in query_results:
    #     print(doc)
    pass
