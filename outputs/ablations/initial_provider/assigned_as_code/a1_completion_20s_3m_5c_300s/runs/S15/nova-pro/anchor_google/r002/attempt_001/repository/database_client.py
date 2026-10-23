import os
from google.cloud import firestore


def get_client():
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    return firestore.Client(project=project_id)


def get_config():
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT'),
        'collection': os.getenv('COLLECTION_NAME')
    }