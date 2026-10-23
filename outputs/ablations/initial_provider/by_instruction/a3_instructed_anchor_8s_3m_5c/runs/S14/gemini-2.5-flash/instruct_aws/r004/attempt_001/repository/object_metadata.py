from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name,
            Key=request.object_name
        )

        return ObjectMetadataResponse(
            object_name=request.object_name,
            last_modified=response['LastModified'].isoformat(),
            size=response['ContentLength'],
            content_type=response['ContentType'],
            e_tag=response['ETag'].strip('\"'),
            metadata=response.get('Metadata', {})
        )
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NotFound':
            raise FileNotFoundError(f"Object {request.object_name} not found in bucket {request.bucket_name}")
        else:
            raise RuntimeError(f"Error retrieving object metadata: {e}")
