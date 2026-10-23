from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from datetime import datetime

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    """Reads object metadata or head information from AWS S3 managed object storage.

    Args:
        request: An ObjectMetadataRequest containing bucket and key.

    Returns:
        An ObjectMetadataResponse with the object's metadata.
    """
    s3_client = get_s3_client()

    response = s3_client.head_object(
        Bucket=request.bucket_name,
        Key=request.object_key
    )

    content_type = response.get('ContentType', 'application/octet-stream')
    content_length = response.get('ContentLength', 0)
    last_modified_dt = response.get('LastModified', datetime.min) # type: ignore
    etag = response.get('ETag', '').strip('\"')
    custom_metadata = {k.lower(): v for k, v in response.get('Metadata', {}).items()}

    return ObjectMetadataResponse(
        content_type=content_type,
        content_length=content_length,
        last_modified=last_modified_dt,
        etag=etag,
        custom_metadata=custom_metadata
    )
