from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectMetadata, normalize_metadata


def object_metadata(bucket=None, key=None):
    client = get_s3_client()
    response = client.head_object(Bucket=get_bucket_name(bucket), Key=key)
    return ObjectMetadata(
        bucket=get_bucket_name(bucket),
        key=key,
        size=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=response.get("LastModified"),
        metadata=normalize_metadata(response.get("Metadata")),
    )
