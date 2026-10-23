from storage_client import get_bucket
from storage_models import normalize_blob_list, normalize_prefix


def list_objects(bucket: str, prefix: str = None):
    normalized_prefix = normalize_prefix(prefix)
    blobs = get_bucket(bucket).list_blobs(prefix=normalized_prefix)
    return normalize_blob_list(blobs)
