import os
from google.cloud import firestore

def query_documents(collection_name: str, field_name: str, field_value: str):
    """
    Queries documents in a Firestore collection by a field value.

    Args:
        collection_name: The name of the Firestore collection.
        field_name: The name of the field to query by.
        field_value: The value of the field to match.
    """
    # Initialize Firestore client
    # Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or authenticate otherwise, e.g., 'gcloud auth application-default login'
    db = firestore.Client()

    print(f"Querying collection: {collection_name} for documents where {field_name} == {field_value}")

    # Create a reference to the collection
    collection_ref = db.collection(collection_name)

    # Create a query against the collection
    query = collection_ref.where(field_name, "==", field_value)

    # Execute the query and get the results
    results = query.stream()

    found_documents = False
    for doc in results:
        print(f"Document ID: {doc.id}, Data: {doc.to_dict()}")
        found_documents = True
    
    if not found_documents:
        print("No documents found matching the criteria.")

if __name__ == "__main__":
    # Example usage:
    # Replace 'your-collection-name', 'your-field-name', and 'your-field-value' with actual values
    # For a partition-style key, you might query on a specific field that acts as a partition key.
    # For example, if you have a 'city' field and want to query all documents for 'San Francisco':
    # query_documents("cities", "name", "San Francisco")
    
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up, or run in a GCP environment with appropriate permissions.
    # For local testing, you might need to:
    # 1. Install google-cloud-firestore: pip install google-cloud-firestore
    # 2. Authenticate: gcloud auth application-default login
    
    # Example 1: Querying by a simple field value
    # Uncomment and replace with your actual collection and field details to run
    # query_documents("users", "city", "New York")

    # Example 2: Querying for documents where a field matches a specific value (can act as a partition key)
    # Uncomment and replace with your actual collection and field details to run
    # query_documents("products", "category", "electronics")
    
    print("To run this script, please uncomment the example usage in the if __name__ == '__main__': block and replace placeholder values with your actual Firestore collection and field names.")
    print("Also, ensure you have authenticated with Google Cloud and have the 'google-cloud-firestore' library installed.")
