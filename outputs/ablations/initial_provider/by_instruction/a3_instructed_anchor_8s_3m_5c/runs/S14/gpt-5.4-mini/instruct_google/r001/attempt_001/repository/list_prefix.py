from storage_client import get_bucket
from storage_models import normalize_object_names, normalize_prefix


def list_objects_with_prefix(bucket: str, prefix: str):
    prefix = normalize_prefix(prefix)
    return normalize_object_names(blob.name for blob in get_bucket(bucket).list_blobs(prefix=prefix))
