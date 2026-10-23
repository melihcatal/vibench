from storage_client import get_storage_client
from storage_models import ObjectMetadata, ObjectListResponse
from botocore.exceptions import ClientError

def list_prefix(bucket: str, prefix: str = '') -> ObjectListResponse:
    """
    Lists objects under a prefix in Amazon S3 bucket.
    """
    client = get_storage_client()
    try:
        response = client.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
        contents = []
        for obj in response.get('Contents', []):
            contents.append(ObjectMetadata(
                key=obj['Key'],
                e_tag=obj['ETag'],
                size=obj['Size'],
                last_modified=obj['LastModified']
            ))
        return ObjectListResponse(
            contents=contents,
            is_truncated=response.get('IsTruncated', False),
            next_continuation_token=response.get('NextContinuationToken')
        )
    except ClientError as e:
        raise ValueError(f"Error listing objects: {e}")