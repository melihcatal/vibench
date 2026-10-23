import os
from typing import List, Dict, Any
from google.cloud import firestore # Provider-identifying signal
from database_client import get_firestore_client
from database_models import DocumentData

def query_documents(collection_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
    """
    Queries documents by a field value from Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field, '==', value).stream()

    results = []
    for doc in docs:
        results.append({"id": doc.id, **doc.to_dict()})
    
    print(f"Found {len(results)} documents in collection {collection_name} where {field} == {value}.")
    return results

if __name__ == '__main__':
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables
    # before running this example.
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.getenv('GOOGLE_CLOUD_PROJECT', 'your-gcp-project-id') # Replace with your project ID

    test_collection = "my_documents"
    # First, ensure there's data to query
    from upsert_document import upsert_document
    upsert_document(test_collection, "doc_query_1", {"name": "Query Doc 1", "category": "A"})
    upsert_document(test_collection, "doc_query_2", {"name": "Query Doc 2", "category": "B"})
    upsert_document(test_collection, "doc_query_3", {"name": "Query Doc 3", "category": "A"})

    print("\nQuerying documents...")
    query_results = query_documents(test_collection, "category", "A")

    if query_results:
        print("Query results:")
        for doc in query_results:
            print(doc)
    else:
        print("No documents matched the query.")
