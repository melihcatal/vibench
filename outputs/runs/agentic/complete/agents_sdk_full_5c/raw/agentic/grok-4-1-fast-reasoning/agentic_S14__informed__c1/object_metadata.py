from typing import Dict, Any
from storage_client import get_s3_client

def object_metadata(bucket: str, object_key: str) -> Dict[str, Any]:
    """
    Reads object metadata (HEAD) from Amazon S3.
    """
    client = get_s3_client()
    response = client.head_object(Bucket=bucket, Key=object_key)
    return dict(response)