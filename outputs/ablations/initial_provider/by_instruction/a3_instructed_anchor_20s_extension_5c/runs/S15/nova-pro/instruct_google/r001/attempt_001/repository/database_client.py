import google.cloud.firestore as firestore

def get_firestore_client():
    return firestore.Client()

def normalize_document(document):
    return {k: v for k, v in document.items() if not k.startswith('__')}