# Retrieve object metadata / HEAD information from Managed Object Storage (AWS S3 provider)
import os
from storage_client import create_s3_client
from storage_models import ObjectMetadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    """HEAD the object and return a normalized metadata record."""
    client = create_s3_client()
    head = client.head_object(Bucket=bucket, Key=key)

    return ObjectMetadata(
        name=head["Key"],
        size=head["ContentLength"],
        last_modified=str(head["LastModified"]),
        content_type=head.get("ContentType", ""),
    )
