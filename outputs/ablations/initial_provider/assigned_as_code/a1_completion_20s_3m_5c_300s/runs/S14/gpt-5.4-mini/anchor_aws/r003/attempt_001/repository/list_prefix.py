from storage_client import storage_client, storage_config
from storage_models import normalize_listing


def list_prefix(payload=None, config=None):
    cfg = storage_config(config)
    payload = payload or {}
    client = storage_client(cfg)
    response = client.list_objects_v2(
        Bucket=cfg["bucket"],
        Prefix=payload.get("prefix", cfg.get("prefix", "")),
    )
    return {"objects": normalize_listing(response.get("Contents", []))}
