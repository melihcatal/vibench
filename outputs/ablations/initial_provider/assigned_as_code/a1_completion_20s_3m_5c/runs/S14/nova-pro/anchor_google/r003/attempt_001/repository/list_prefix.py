from storage_client import get_storage_client
from storage_models import normalize_blob


def list_prefix(prefix, config=None):
    client = get_storage_client(config)
    blobs = client.list_blobs(config["bucket"], prefix=prefix)
    return [normalize_blob(blob) for blob in blobs]