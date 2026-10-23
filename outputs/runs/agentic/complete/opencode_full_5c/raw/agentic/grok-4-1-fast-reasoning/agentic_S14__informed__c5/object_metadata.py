from storage_client import get_s3_client
from storage_models import normalize_object_metadata


def object_metadata(bucket_name: str, object_name: str) -> dict:
    client = get_s3_client()
    raw = client.head_object(Bucket=bucket_name, Key=object_name)
    return normalize_object_metadata(raw)
