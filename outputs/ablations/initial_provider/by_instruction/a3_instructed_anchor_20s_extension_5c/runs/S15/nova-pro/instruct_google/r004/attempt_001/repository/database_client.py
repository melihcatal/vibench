import google.cloud.firestore as firestore

def get_firestore_client():
    return firestore.Client()