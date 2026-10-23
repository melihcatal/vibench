import logging
from botocore.exceptions import ClientError
from storage_client import get_s3_client, get_storage_bucket

def create_presigned_download_url(object_key: str, expiration: int = 3600, bucket_name: str = None) -> str:
    """
    Generate a presigned URL to share an S3 object.

    :param object_key: Key of the object to generate a URL for.
    :param expiration: Time in seconds for the presigned URL to remain valid.
    :param bucket_name: The S3 bucket. If None, uses default from env.
    :return: The presigned URL as a string. If error, returns None.
    """
    s3_client = get_s3_client()
    target_bucket = bucket_name or get_storage_bucket()

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': target_bucket, 'Key': object_key},
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(f"Failed to generate presigned URL for {object_key} in {target_bucket}: {e}")
        raise
    
    return response
