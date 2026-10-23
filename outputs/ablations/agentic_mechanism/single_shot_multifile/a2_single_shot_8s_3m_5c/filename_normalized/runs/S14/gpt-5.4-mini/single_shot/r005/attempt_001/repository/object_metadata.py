from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse, normalize_s3_metadata


def object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    head = s3.head_object(Bucket=bucket, Key=request.key)
    return ObjectMetadataResponse(
        bucket=bucket,
        key=request.key,
        content_length=head.get('ContentLength'),
        content_type=head.get('ContentType'),
        etag=head.get('ETag'),
        last_modified=head.get('LastModified'),
        metadata=normalize_s3_metadata(head.get('Metadata', {})),
    )
