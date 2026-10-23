from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(
    request: ObjectMetadataRequest,
) -> ObjectMetadataResponse:
    """Reads object metadata or head information from AWS S3 managed object storage."""
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name,
            Key=request.object_key,
        )
        # Clean up response to remove non-serializable parts if necessary,
        # and focus on relevant metadata.
        metadata = {
            'ContentLength': response.get('ContentLength'),
            'ContentType': response.get('ContentType'),
            'ETag': response.get('ETag'),
            'LastModified': response.get('LastModified').isoformat() if response.get('LastModified') else None,
            'VersionId': response.get('VersionId'),
            'ServerSideEncryption': response.get('ServerSideEncryption'),
            'Metadata': response.get('Metadata', {}), # Custom metadata
        }
        return ObjectMetadataResponse(
            object_key=request.object_key,
            metadata={k: v for k, v in metadata.items() if v is not None}
        )
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            raise FileNotFoundError(f"Object {request.object_key} not found in bucket {request.bucket_name}") from e
        raise RuntimeError(f"Error retrieving object metadata: {e}") from e
