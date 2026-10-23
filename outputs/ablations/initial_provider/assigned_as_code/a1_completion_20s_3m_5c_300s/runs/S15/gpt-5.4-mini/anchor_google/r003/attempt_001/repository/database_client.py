from google.cloud import firestore, storage


def get_firestore_client(config):
    return firestore.Client(project=config["project_id"])


def get_storage_client(config):
    return storage.Client(project=config["project_id"])


def get_collection_name(config):
    return config["collection"]


def get_bucket_name(config):
    return config["bucket"]
