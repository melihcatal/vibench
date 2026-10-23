from typing import Dict, List, Optional

from storage_client import get_s3_client


def list_prefix(bucket: str, prefix: str = "", region: Optional[str] = None) -> List[Dict[str, str]]:
    s3 = get_s3_client(region)
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [{"key": item["Key"], "etag": item.get("ETag", ""), "size": str(item.get("Size", 0)), "last_modified": item.get("LastModified", "")} for item in response.get("Contents", [])]
