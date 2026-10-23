from storage_client import get_storage_client
from storage_models import ObjectMetadata, normalize_metadata


def get_object_metadata(bucket: str, object_key: str) -> ObjectMetadata:
    client = get_storage_client()
    response = client.head_object(Bucket=bucket, Key=object_key)
    return normalize_metadata(response)
