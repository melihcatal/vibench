from storage_client import storage_client
from storage_models import normalize_listing


def list_prefix(payload, config=None):
    client, config = storage_client(config)
    prefix = payload.get("prefix", config.get("prefix", ""))
    iterator = client.bucket(config["bucket"]).list_blobs(prefix=prefix)
    return {"objects": normalize_listing(iterator)}
