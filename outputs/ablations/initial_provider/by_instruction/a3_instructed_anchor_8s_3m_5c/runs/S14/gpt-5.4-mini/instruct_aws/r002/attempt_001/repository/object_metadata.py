from storage_client import default_bucket, s3_client
from storage_models import normalize_key, response_payload


def object_metadata(bucket=None, key=None):
    bucket_name = default_bucket(bucket)
    object_key = normalize_key(key)
    head = s3_client().head_object(Bucket=bucket_name, Key=object_key)
    return response_payload(
        provider="aws",
        service="s3",
        bucket=bucket_name,
        key=object_key,
        etag=head.get("ETag"),
        content_length=head.get("ContentLength"),
        content_type=head.get("ContentType"),
        last_modified=head.get("LastModified"),
        metadata=head.get("Metadata"),
        storage_class=head.get("StorageClass"),
        version_id=head.get("VersionId"),
    )
