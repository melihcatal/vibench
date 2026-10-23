from google.cloud import firestore, storage


def get_firestore_client(config=None):
    config = config or {}
    return firestore.Client(project=config["project_id"])


def get_storage_client(config=None):
    config = config or {}
    return storage.Client(project=config["project_id"])


def get_collection_ref(config=None):
    config = config or {}
    return get_firestore_client(config).collection(config["collection"])
