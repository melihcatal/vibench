from storage_client import get_bucket_name, get_s3_client, load_storage_config
from storage_models import normalize_object_name


def list_prefix(payload, config=None):
    config = load_storage_config(config)
    client = get_s3_client(config)
    response = client.list_objects_v2(Bucket=get_bucket_name(config), Prefix=normalize_object_name(payload.get("prefix", "")))
    return {"objects": [{"key": item["Key"], "size": item.get("Size"), "etag": item.get("ETag"), "last_modified": item.get("LastModified").isoformat() if item.get("LastModified") else None} for item in response.get("Contents", [])]}
