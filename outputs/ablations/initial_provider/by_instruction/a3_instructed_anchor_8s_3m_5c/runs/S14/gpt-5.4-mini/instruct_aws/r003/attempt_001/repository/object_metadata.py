from typing import Any, Dict, Optional

from storage_client import get_s3_client
from storage_models import metadata_from_head


def object_metadata(bucket: str, key: str, region: Optional[str] = None) -> Dict[str, Any]:
    s3 = get_s3_client(region)
    response = s3.head_object(Bucket=bucket, Key=key)
    return metadata_from_head(response)
