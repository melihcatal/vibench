from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_object_metadata


def get_object_metadata(bucket=None, key=None):
    client = get_s3_client()
    response = client.head_object(Bucket=bucket or get_bucket_name(), Key=key)
    return normalize_object_metadata(bucket or get_bucket_name(), key, response)
