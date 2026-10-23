import boto3
from storage_models import ObjectMetadataResult

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadataResult:
    """Retrieve metadata/HEAD information for an S3 object.

    Uses boto3 client; credentials from AWS_ACCESS_KEY_ID/SECRET_ACCESS_KEY.
    """
    s3 = boto3.client('s3')
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    # Normalize to a simple dict
    metadata = response.get('Metadata', {})
    return ObjectMetadataResult(
        size=response.get('ContentLength'),
        content_type=response.get('ContentType'),
        last_modified=response.get('LastModified'),
        custom_metadata=metadata
    )
