from storage_client import get_storage_client
from storage_models import normalize_blob


def object_metadata(object_name, config=None):
    client = get_storage_client(config)
    blob = client.bucket(config["bucket"]).blob(object_name)
    blob.reload()
    return normalize_blob(blob)