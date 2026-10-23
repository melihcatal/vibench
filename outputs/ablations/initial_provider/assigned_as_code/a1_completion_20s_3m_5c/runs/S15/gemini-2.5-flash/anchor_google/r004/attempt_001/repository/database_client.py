from google.cloud import firestore

def get_firestore_client(project_id):
    return firestore.Client(project=project_id)
