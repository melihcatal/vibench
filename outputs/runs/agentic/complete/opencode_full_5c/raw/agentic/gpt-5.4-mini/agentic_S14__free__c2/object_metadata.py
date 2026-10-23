from storage_client import storage_client
from storage_models import HeadObjectResponse


def object_metadata(bucket: str, object_name: str) -> HeadObjectResponse:
    client = storage_client("s3")
    result = client.head_object(Bucket=bucket, Key=object_name)
    return HeadObjectResponse(
        bucket=bucket,
        object_name=object_name,
        content_length=result.get("ContentLength"),
        content_type=result.get("ContentType"),
        last_modified=str(result.get("LastModified"))
        if result.get("LastModified")
        else None,
        etag=result.get("ETag"),
        metadata=result.get("Metadata", {}),
        raw=result,
    )
