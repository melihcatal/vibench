from storage_client import get_bucket
from storage_models import normalize_prefix


def list_prefix(payload, config=None):
    bucket, _ = get_bucket(config)
    prefix = normalize_prefix(payload)
    blobs = bucket.list_blobs(prefix=prefix)
    return {"objects": [{"object_name": blob.name, "size": blob.size, "updated": blob.updated} for blob in blobs], "prefix": prefix}
