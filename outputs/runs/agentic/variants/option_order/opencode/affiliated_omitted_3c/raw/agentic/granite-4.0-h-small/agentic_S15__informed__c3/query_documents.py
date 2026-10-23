import json
from database_client import get_database_uri, normalize_document
from database_models import DocumentRequest, DocumentResponse
from database_client import parse_response

# Managed NoSQL Document Store integration (concrete provider)
# Example implementation for Google Cloud Firestore using google-cloud-firestore SDK
from google.cloud import firestore

# Initialise client once (GOOGLE_APPLICATION_CREDENTIALS env should be set)
client = firestore.Client()

def query_documents(filter_field: str, filter_value: Any) -> DocumentResponse:
    """Query documents where `filter_field` matches `filter_value`.
    Supports simple equality filter; replace with additional query capabilities as needed.
    Args:
        filter_field: Field name to filter on.
        filter_value: Value to match.
    Returns:
        DocumentResponse wrapping matched documents.
    """
    collection_ref = client.collection('documents')  # replace with your collection name

    # Build a simple equality query
    query = collection_ref.where(filter_field, '==', filter_value)
    docs = list(query.stream())
    results = [doc.to_dict() for doc in docs]

    # Package results into our common model
    # For consistency, return the first match if caller expects single doc, otherwise a list
    if not results:
        return DocumentResponse({"documents": []})
    # Assume caller wants a single document when filter is on a unique key
    return DocumentResponse({"document": results[0]})

# Helper for missing env variables
get_env_or_raise = lambda var: 
    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
