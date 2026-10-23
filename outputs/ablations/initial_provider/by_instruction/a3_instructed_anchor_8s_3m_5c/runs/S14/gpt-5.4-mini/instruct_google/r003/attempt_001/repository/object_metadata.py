from storage_client import get_bucket
from storage_models import normalize_blob_metadata


def get_object_metadata(bucket: str, object_name: str):
    blob = get_bucket(bucket).blob(object_name)
    blob.reload()
    return normalize_blob_metadata(blob)
