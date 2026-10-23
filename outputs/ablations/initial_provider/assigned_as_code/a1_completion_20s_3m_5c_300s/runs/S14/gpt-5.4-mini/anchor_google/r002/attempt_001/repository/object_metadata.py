from storage_client import get_bucket
from storage_models import normalize_object_name, to_object_response


def object_metadata(payload, config=None):
    bucket = get_bucket(config)
    blob = bucket.blob(normalize_object_name(payload))
    blob.reload()
    return to_object_response(blob)
