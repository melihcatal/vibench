from storage_client import get_s3_client, get_bucket_name
from storage_models import ObjectMetadata

def get_object_metadata(
    bucket_name: str | None = None,
    key: str
) -> ObjectMetadata:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    client = get_s3_client()
    resp = client.head_object(Bucket=bucket_name, Key=key)
    return {
        "etag": resp["ETag"].strip('"'),
        "size": resp["ContentLength"],
        "content_type": resp.get("ContentType"),
        "last_modified": str(resp["LastModified"]),
        "metadata": resp.get("Metadata", {})
    }
