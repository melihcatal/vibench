from storage_client import storage_client
from storage_models import normalize_metadata


def object_metadata(payload, config=None):
    client, config = storage_client(config)
    blob = client.bucket(config["bucket"]).blob(payload["object_name"])
    blob.reload()
    return normalize_metadata(blob)
