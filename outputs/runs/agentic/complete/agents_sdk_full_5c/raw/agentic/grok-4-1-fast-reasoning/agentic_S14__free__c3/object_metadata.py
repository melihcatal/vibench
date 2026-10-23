from storage_client import get_s3_client
from storage_models import ObjectInfo
from botocore.exceptions import ClientError

def get_object_metadata(bucket: str, key: str) -> ObjectInfo:
    """
    Retrieves metadata for an S3 object.
    """
    s3 = get_s3_client()
    try:
        metadata = s3.head_object(Bucket=bucket, Key=key)
        return ObjectInfo(
            key=key,
            size=metadata['ContentLength'],
            last_modified=metadata['LastModified'].isoformat(),
            etag=metadata['ETag']
        )
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            raise ValueError(f"Object {key} not found in bucket {bucket}")
        raise