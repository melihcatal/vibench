from typing import Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectMetadataResponse, normalize_metadata, normalize_timestamp


def get_object_metadata(object_key: str, bucket: Optional[str] = None) -> ObjectMetadataResponse:
    bucket_name = bucket or get_bucket_name()
    client = get_s3_client()
    head = client.head_object(Bucket=bucket_name, Key=object_key)
    return ObjectMetadataResponse(bucket=bucket_name, key=object_key, size=head.get('ContentLength'), content_type=head.get('ContentType'), etag=head.get('ETag'), last_modified=normalize_timestamp(head.get('LastModified')), metadata=normalize_metadata(head.get('Metadata')), version_id=head.get('VersionId'))
