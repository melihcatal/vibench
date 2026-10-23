from google.cloud import firestore

def get_firestore_client(project_id: str):
    return firestore.Client(project=project_id)

def get_collection_ref(client, collection_name: str):
    return client.collection(collection_name)
