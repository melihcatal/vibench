from storage_client import get_s3_client, get_storage_config
from storage_models import normalize_prefix


def list_prefix(payload, config=None):
    config = get_storage_config(config)
    client = get_s3_client(config)
    response = client.list_objects_v2(Bucket=config["bucket"], Prefix=normalize_prefix(payload))
    return {"objects": [item["Key"] for item in response.get("Contents", [])], "prefix": normalize_prefix(payload)}
