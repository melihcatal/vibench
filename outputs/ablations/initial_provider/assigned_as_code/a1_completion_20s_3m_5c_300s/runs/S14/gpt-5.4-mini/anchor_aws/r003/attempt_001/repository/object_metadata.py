from storage_client import storage_client, storage_config
from storage_models import normalize_metadata


def object_metadata(payload, config=None):
    cfg = storage_config(config)
    client = storage_client(cfg)
    head = client.head_object(Bucket=cfg["bucket"], Key=payload["object_name"])
    head["Key"] = payload["object_name"]
    return normalize_metadata(head)
