import logging
from typing import IO
from botocore.exceptions import ClientError
from storage_client import get_s3_client, get_storage_bucket
from storage_models import UploadResult

def upload_object_to_s3(file_stream: IO[bytes], object_key: str, bucket_name: str = None) -> UploadResult:
    """
    Uploads a file-like object to an S3 bucket.

    :param file_stream: Binary file stream to upload.
    :param object_key: The key (path) for the object in the bucket.
    :param bucket_name: The target S3 bucket. If None, uses default from env.
    :return: An UploadResult containing details of the upload.
    """
    s3_client = get_s3_client()
    target_bucket = bucket_name or get_storage_bucket()

    try:
        s3_client.upload_fileobj(file_stream, target_bucket, object_key)
        
        # To get ETag and VersionId, a separate head_object call is often needed after upload
        response = s3_client.head_object(Bucket=target_bucket, Key=object_key)
        
        return UploadResult(
            bucket=target_bucket,
            key=object_key,
            e_tag=response.get('ETag', '').strip('"'),
            version_id=response.get('VersionId')
        )

    except ClientError as e:
        logging.error(f"Failed to upload {object_key} to {target_bucket}: {e}")
        raise
