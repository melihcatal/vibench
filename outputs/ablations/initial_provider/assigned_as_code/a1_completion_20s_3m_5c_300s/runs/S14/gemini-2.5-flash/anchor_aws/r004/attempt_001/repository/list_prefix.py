import boto3
from storage_client import get_s3_client
from storage_models import StorageConfig, ListObjectsRequest

def list_prefix(request: ListObjectsRequest, config: StorageConfig):
    s3_client = get_s3_client(config)
    response = s3_client.list_objects_v2(
        Bucket=config.bucket,
        Prefix=request.prefix,
        MaxKeys=request.max_keys
    )
    contents = response.get('Contents', [])
    object_names = [obj['Key'] for obj in contents]
    return {"object_names": object_names}
