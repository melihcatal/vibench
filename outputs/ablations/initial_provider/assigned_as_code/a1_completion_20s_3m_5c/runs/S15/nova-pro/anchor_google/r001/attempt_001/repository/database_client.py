from google.cloud import firestore

def get_firestore_client(project_id):
    return firestore.Client(project=project_id)

def normalize_document(document):
    return {k: v for k, v in document.items() if not k.startswith('__')}