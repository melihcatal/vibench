from storage_client import create_s3_client, resolve_bucket
from storage_models import ObjectMetadataRequest, normalize_object_result


def object_metadata(bucket: str, key: str):
    request = ObjectMetadataRequest(bucket=bucket, key=key).normalize()
    s3 = create_s3_client()
    response = s3.head_object(Bucket=resolve_bucket(request.bucket), Key=request.key)
    return normalize_object_result(
        {
            "bucket": request.bucket,
            "key": request.key,
            "etag": response.get("ETag"),
            "version_id": response.get("VersionId"),
            "content_type": response.get("ContentType"),
            "content_length": response.get("ContentLength"),
            "metadata": response.get("Metadata", {}),
        }
    )
