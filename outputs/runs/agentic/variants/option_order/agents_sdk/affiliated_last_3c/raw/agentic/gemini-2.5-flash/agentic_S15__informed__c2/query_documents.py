import os
from google.cloud import firestore

def query_documents(collection_name: str, field_name: str, field_value: any):
    """Queries documents by a field value in Firestore."""
    db = firestore.Client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    results = []
    for doc in docs:
        results.append({"id": doc.id, **doc.to_dict()})
    return {"status": "success", "documents": results}

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # and Firestore is set up for your project.
    # collection = "my_collection"
    # field = "active"
    # value = True
    # result = query_documents(collection, field, value)
    # print(result)
    pass
