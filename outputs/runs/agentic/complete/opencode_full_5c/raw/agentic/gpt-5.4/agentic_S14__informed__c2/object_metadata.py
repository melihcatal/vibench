from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ObjectMetadataResult


def get_object_metadata(bucket_name: str, object_name: str) -> ObjectMetadataResult:
    s3_client = get_s3_client()
    head = s3_client.head_object(Bucket=bucket_name, Key=object_name)
    return ObjectMetadataResult.from_s3_head(
        bucket_name=bucket_name, object_name=object_name, head=head
    )
