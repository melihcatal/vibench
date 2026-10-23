from storage_client import load_storage_config, s3_client
from storage_models import normalize_list_item


def list_prefix(bucket: str, prefix: str = ""):
    config = load_storage_config(bucket)
    client = s3_client()
    response = client.list_objects_v2(Bucket=config.bucket, Prefix=prefix)
    contents = response.get("Contents", [])
    return [normalize_list_item(item) for item in contents]
