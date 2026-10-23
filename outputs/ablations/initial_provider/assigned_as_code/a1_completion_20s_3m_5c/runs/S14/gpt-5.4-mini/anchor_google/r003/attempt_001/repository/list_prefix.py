from storage_client import storage_bucket, load_config
from storage_models import object_listing


def list_prefix(payload, config=None):
    config = load_config(config)
    prefix = (payload or {}).get("prefix", "")
    blobs = storage_bucket(config).list_blobs(prefix=prefix)
    return {"objects": object_listing(blobs)}
