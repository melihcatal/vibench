import logging
from botocore.exceptions import ClientError
from storage_client import get_s3_client, get_storage_bucket
from storage_models import ObjectMetadata

def get_object_metadata(object_key: str, bucket_name: str = None) -> ObjectMetadata:
    """
    Retrieves metadata for an object from an S3 bucket.

    :param object_key: The key of the object.
    :param bucket_name: The S3 bucket. If None, uses default from env.
    :return: An ObjectMetadata object.
    """
    s3_client = get_s3_client()
    target_bucket = bucket_name or get_storage_bucket()

    try:
        response = s3_client.head_object(Bucket=target_bucket, Key=object_key)
        
        return ObjectMetadata(
            key=object_key,
            content_length=response['ContentLength'],
            content_type=response['ContentType'],
            last_modified=response['LastModified'].isoformat(),
            e_tag=response['ETag'].strip('"'),
            metadata=response.get('Metadata', {})
        )
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.warning(f"Object {object_key} not found in bucket {target_bucket}.")
            raise FileNotFoundError(f"Object not found: {object_key}")
        else:
            logging.error(f"Error getting metadata for {object_key}: {e}")
            raise
