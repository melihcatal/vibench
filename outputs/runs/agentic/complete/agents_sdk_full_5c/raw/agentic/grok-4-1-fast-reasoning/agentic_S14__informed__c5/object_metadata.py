from storage_client import get_storage_client
from typing import Dict, Any
from botocore.exceptions import ClientError

def get_object_metadata(bucket: str, key: str) -&gt; Dict[str, Any]:
    """
    Read object metadata from Amazon S3 using head_object.
    """
    client = get_storage_client()
    try:
        metadata = client.head_object(Bucket=bucket, Key=key)
        return dict(metadata)
    except ClientError as e:
        raise ValueError(f"S3 head_object failed: {e}")