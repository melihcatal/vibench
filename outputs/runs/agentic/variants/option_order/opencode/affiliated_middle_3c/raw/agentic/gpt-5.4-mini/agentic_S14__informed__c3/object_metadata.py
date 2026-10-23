import boto3

from storage_client import resolve_bucket
from storage_models import ObjectMetadata


def get_object_metadata(bucket: str, key: str):
    client = boto3.client("s3")
    response = client.head_object(Bucket=resolve_bucket(bucket), Key=key)
    return ObjectMetadata(
        bucket=resolve_bucket(bucket),
        key=key,
        size=response.get("ContentLength"),
        etag=response.get("ETag"),
        content_type=response.get("ContentType"),
        last_modified=str(response.get("LastModified"))
        if response.get("LastModified")
        else None,
        extra={
            k: v
            for k, v in response.items()
            if k not in {"ContentLength", "ETag", "ContentType", "LastModified"}
        },
    )
