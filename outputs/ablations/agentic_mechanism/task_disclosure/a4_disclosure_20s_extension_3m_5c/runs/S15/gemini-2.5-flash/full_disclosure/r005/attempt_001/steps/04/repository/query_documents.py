from google.cloud import firestore
import os

def query_documents(collection_name: str, field_name: str, field_value: str, project_id: str = None):
    """
    Queries documents in a Firestore collection by a field value.

    Args:
        collection_name: The name of the Firestore collection.
        field_name: The name of the field to query.
        field_value: The value of the field to match.
        project_id: The Google Cloud project ID. If None, it will be inferred from the environment.

    Returns:
        A list of dictionaries, where each dictionary represents a document.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    db = firestore.Client(project=project_id)
    
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()

    results = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id  # Include document ID
        results.append(doc_data)
    
    return results

if __name__ == '__main__':
    # Example Usage (replace with your actual collection and field details)
    # Set your Google Cloud project ID as an environment variable or pass it directly
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    # Example: Query documents in 'my_collection' where 'status' field is 'active'
    # documents = query_documents("my_collection", "status", "active")
    # for doc in documents:
    #     print(f"Document ID: {doc.get("id")}, Data: {doc}")

    print("Firebase Firestore client configured. Use query_documents function to query documents.")
