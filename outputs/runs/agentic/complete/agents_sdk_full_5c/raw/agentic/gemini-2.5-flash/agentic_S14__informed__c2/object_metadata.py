import boto3
from storage_client import get_s3_client, get_s3_bucket_name
from storage_models import ObjectMetadataRequest, ObjectMetadata

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadata:
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=request.object_key)
        return ObjectMetadata(
            object_key=request.object_key,
            size=response['ContentLength'],
            last_modified=response['LastModified'].isoformat(),
            content_type=response.get('ContentType', 'application/octet-stream'),
            etag=response['ETag'].strip('\'\''),
            metadata=response.get('Metadata', {}),
        )
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NotFound':
            raise FileNotFoundError(f"Object {request.object_key} not found in bucket {bucket_name}")
        else:
            raise RuntimeError(f"Failed to retrieve object metadata: {e}")
