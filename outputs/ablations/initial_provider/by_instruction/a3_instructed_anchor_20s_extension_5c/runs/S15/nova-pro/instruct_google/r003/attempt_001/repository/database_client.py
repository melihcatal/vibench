from google.cloud import firestore

def get_client():
    return firestore.client()