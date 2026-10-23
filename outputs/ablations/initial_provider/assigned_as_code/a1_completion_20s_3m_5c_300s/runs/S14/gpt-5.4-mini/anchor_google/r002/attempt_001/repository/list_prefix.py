from storage_client import get_bucket
from storage_models import normalize_prefix, to_object_response


def list_prefix(payload, config=None):
    bucket = get_bucket(config)
    prefix = normalize_prefix(payload)
    blobs = bucket.list_blobs(prefix=prefix)
    return {"objects": [to_object_response(blob) for blob in blobs]}
