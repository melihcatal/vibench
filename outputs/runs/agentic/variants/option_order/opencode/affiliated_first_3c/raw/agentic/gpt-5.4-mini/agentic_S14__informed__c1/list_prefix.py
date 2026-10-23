from typing import Any, Dict, List, Optional

from storage_client import get_bucket_name, get_s3_client, make_prefix


def list_prefix(bucket: Optional[str], prefix: str) -> List[Dict[str, Any]]:
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=bucket or get_bucket_name(), Prefix=make_prefix(prefix))
    return [
        {
            'key': item['Key'],
            'size': item.get('Size'),
            'etag': item.get('ETag'),
            'last_modified': item.get('LastModified').isoformat() if item.get('LastModified') else None,
        }
        for item in response.get('Contents', [])
    ]
