import os
from google.cloud import firestore

def query_documents(collection_name: str, field: str, value: str):
    """
    Queries documents by a field value from a Google Cloud Firestore collection.

    Args:
        collection_name: The name of the Firestore collection.
        field: The field to query by.
        value: The value to match.

    Returns:
        A list of dictionaries, where each dictionary represents a document.
    """
    # Initialize Firestore client
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    db = firestore.Client()

    docs = db.collection(collection_name).where(field, "==", value).stream()
    
    results = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id  # Add the document ID to the data
        results.append(doc_data)
    
    return results

def query_documents_by_partition_key(collection_name: str, partition_key_field: str, partition_key_value: str):
    """
    Queries documents by a partition-style key from a Google Cloud Firestore collection.

    Args:
        collection_name: The name of the Firestore collection.
        partition_key_field: The field representing the partition key.
        partition_key_value: The value of the partition key.

    Returns:
        A list of dictionaries, where each dictionary represents a document.
    """
    db = firestore.Client()

    docs = db.collection(collection_name).where(partition_key_field, "==", partition_key_value).stream()

    results = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        results.append(doc_data)
    
    return results
