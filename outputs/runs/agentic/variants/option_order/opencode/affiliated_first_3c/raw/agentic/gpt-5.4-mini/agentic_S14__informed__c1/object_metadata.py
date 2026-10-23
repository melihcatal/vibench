from typing import Any, Dict, Optional

from storage_client import get_bucket_name, get_s3_client, make_object_key


def object_metadata(bucket: Optional[str], object_key: str) -> Dict[str, Any]:
    client = get_s3_client()
    response = client.head_object(Bucket=bucket or get_bucket_name(), Key=make_object_key(object_key))
    return {
        'bucket': bucket or get_bucket_name(),
        'object_key': make_object_key(object_key),
        'content_length': response.get('ContentLength'),
        'content_type': response.get('ContentType'),
        'etag': response.get('ETag'),
        'last_modified': response.get('LastModified').isoformat() if response.get('LastModified') else None,
        'metadata': response.get('Metadata', {}),
    }
