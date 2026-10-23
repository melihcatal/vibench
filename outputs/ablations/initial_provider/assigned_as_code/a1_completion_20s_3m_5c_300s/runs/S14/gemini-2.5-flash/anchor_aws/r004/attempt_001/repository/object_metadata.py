import boto3
from storage_client import get_s3_client
from storage_models import StorageConfig, ObjectMetadataRequest

def object_metadata(request: ObjectMetadataRequest, config: StorageConfig):
    s3_client = get_s3_client(config)
    response = s3_client.head_object(Bucket=config.bucket, Key=request.object_name)
    # Filter out botocore-specific metadata
    metadata = {k: v for k, v in response.items() if not k.startswith('ResponseMetadata')}
    return metadata
