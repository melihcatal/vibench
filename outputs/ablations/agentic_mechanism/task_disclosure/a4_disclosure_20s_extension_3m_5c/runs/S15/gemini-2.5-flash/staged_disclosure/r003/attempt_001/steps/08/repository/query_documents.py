import os
from google.cloud import firestore

def query_documents(collection_name: str, field_name: str, field_value: str):
    """
    Queries documents in a Firestore collection by a specific field value.

    Args:
        collection_name: The name of the Firestore collection.
        field_name: The name of the field to query.
        field_value: The value to match for the specified field.

    Returns:
        A list of dictionaries, where each dictionary represents a document.
    """
    # Initialize Firestore client
    # Make sure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise.
    db = firestore.Client()

    docs = (
        db.collection(collection_name)
        .where(field_name, "==", field_value)
        .stream()
    )

    results = []
    for doc in docs:
        results.append(doc.to_dict())
    return results

def query_documents_by_partition_key(collection_name: str, partition_key_name: str, partition_key_value: str):
    """
    Queries documents in a Firestore collection by a partition-style key.
    This assumes the partition key is a field within the document.

    Args:
        collection_name: The name of the Firestore collection.
        partition_key_name: The name of the field that acts as a partition key.
        partition_key_value: The value of the partition key.

    Returns:
        A list of dictionaries, where each dictionary represents a document.
    """
    db = firestore.Client()

    docs = (
        db.collection(collection_name)
        .where(partition_key_name, "==", partition_key_value)
        .stream()
    )

    results = []
    for doc in docs:
        results.append(doc.to_dict())
    return results

