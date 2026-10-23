from storage_client import get_bucket_client


def list_prefix(payload, config=None):
    config = config or {}
    bucket = get_bucket_client(config)
    prefix = payload.get("prefix", "")
    return {"objects": [blob.name for blob in bucket.list_blobs(prefix=prefix)]}
