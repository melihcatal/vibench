import os
from google.cloud import firestore

def query_documents(collection_name: str, field_name: str, field_value: any):
    """Queries documents by a field value from Firestore."""
    db = firestore.Client()
    docs = db.collection(collection_name).where(field_name, '==', field_value).stream()
    results = []
    for doc in docs:
        results.append({"document_id": doc.id, "data": doc.to_dict()})
    return {"status": "success", "query_field": field_name, "query_value": field_value, "results": results}

if __name__ == '__main__':
    # For demonstration, assume GOOGLE_APPLICATION_CREDENTIALS is set
    # and a Firestore project is configured.
    # Replace 'your_collection', 'your_field', 'your_value' with actual values.
    # This is a placeholder for local execution, not part of the core integration logic.
    pass
