from google.cloud import storage

from storage_client import get_bucket, get_storage_client, load_storage_config
from storage_models import metadata_from_blob, metadata_to_dict, normalize_object_name


def read_object_metadata(object_name: str):
    config = load_storage_config()
    client: storage.Client = get_storage_client()
    bucket = get_bucket(client, config.bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    blob.reload()
    return metadata_to_dict(metadata_from_blob(blob))
