from storage_client import load_storage_config, s3_client
from storage_models import normalize_metadata


def object_metadata(bucket: str, key: str):
    config = load_storage_config(bucket)
    client = s3_client()
    response = client.head_object(Bucket=config.bucket, Key=key)
    return normalize_metadata(response)
