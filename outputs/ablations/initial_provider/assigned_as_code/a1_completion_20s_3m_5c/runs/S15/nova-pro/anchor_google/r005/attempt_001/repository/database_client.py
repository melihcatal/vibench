from google.cloud import firestore


def get_client(config):
    return firestore.Client(project=config["project_id"])


def get_config():
    return {
        "project_id": "your-project-id",
        "collection": "your-collection-name"
    }