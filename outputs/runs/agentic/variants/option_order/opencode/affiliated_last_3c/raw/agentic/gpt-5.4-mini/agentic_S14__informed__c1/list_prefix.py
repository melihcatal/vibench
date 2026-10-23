from google.cloud import storage

from storage_client import get_bucket, get_storage_client, load_storage_config
from storage_models import normalize_object_name


def list_objects(prefix: str = ""):
    config = load_storage_config()
    client: storage.Client = get_storage_client()
    bucket = get_bucket(client, config.bucket_name)
    normalized_prefix = normalize_object_name(prefix)
    return [blob.name for blob in client.list_blobs(bucket, prefix=normalized_prefix)]
