from storage_client import get_storage_client
from storage_models import ObjectMetadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata | None:
    s3_client = get_storage_client()
    try:
        response = s3_client.head_object(Bucket=bucket, Key=key)
        return ObjectMetadata(
            key=key,
            version_id=response.get("VersionId"),
            size=response.get("ContentLength"),
            last_modified=response.get("LastModified").isoformat(),
            content_type=response.get("ContentType"),
            etag=response.get("ETag"),
            metadata=response.get("Metadata"),
        )
    except Exception as e:
        print(f"Error getting object metadata: {e}")
        return None
