from google.cloud import firestore

def query_documents(collection_name: str, field: str, value: str):
    """
    Queries documents by a field value from a Google Cloud Firestore collection.

    Args:
        collection_name: The name of the Firestore collection.
        field: The field to query by.
        value: The value to match for the given field.

    Returns:
        A list of dictionaries, where each dictionary represents a document.
    """
    db = firestore.Client()
    collection_ref = db.collection(collection_name)
    query = collection_ref.where(field, "==", value)
    
    results = []
    for doc in query.stream():
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        results.append(doc_data)
    return results
