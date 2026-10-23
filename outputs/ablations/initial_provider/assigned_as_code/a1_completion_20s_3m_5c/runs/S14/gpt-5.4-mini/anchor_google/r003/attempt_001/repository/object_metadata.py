from storage_client import storage_bucket, load_config
from storage_models import normalize_object_name, metadata_response


def object_metadata(payload, config=None):
    config = load_config(config)
    blob = storage_bucket(config).blob(normalize_object_name(payload))
    blob.reload()
    return metadata_response(blob)
