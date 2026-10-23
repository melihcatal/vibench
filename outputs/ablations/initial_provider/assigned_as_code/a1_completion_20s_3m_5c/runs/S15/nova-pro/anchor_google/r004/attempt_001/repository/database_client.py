from google.cloud import firestore

def get_client(config):
    return firestore.Client(project=config["project_id"])