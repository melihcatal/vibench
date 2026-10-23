from google.cloud import firestore

def query_documents_by_field(collection_name, field_name, field_value):
    db = firestore.Client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    return [doc.to_dict() for doc in docs]

def query_documents_by_partition_key(collection_name, partition_key_name, partition_key_value):
    db = firestore.Client()
    docs = db.collection(collection_name).where(partition_key_name, "==", partition_key_value).stream()
    return [doc.to_dict() for doc in docs]
