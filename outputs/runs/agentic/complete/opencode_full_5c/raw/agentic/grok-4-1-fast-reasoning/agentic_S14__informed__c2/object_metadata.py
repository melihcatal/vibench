from storage_client import get_s3_client
from storage_models import normalize_metadata, ObjectMetadata

def get_object_metadata(bucket: str, key: str) -&gt; ObjectMetadata:
    client = get_s3_client()
    resp = client.head_object(Bucket=bucket, Key=key)
    return normalize_metadata(resp)