import logging
from botocore.exceptions import ClientError
from storage_client import get_storage_client

# Provider: Amazon S3
# SDK: boto3

def upload_object(bucket_name: str, object_key: str, file_path: str) -> bool:
    """
    Uploads a file to an S3 bucket.

    :param bucket_name: The name of the bucket.
    :param object_key: The key (path/filename) for the object in the bucket.
    :param file_path: The local path to the file to upload.
    :return: True if file was uploaded, else False.
    """
    s3_client = get_storage_client()
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        logging.info(f"Successfully uploaded {file_path} to s3://{bucket_name}/{object_key}")
        return True
    except ClientError as e:
        logging.error(f"Failed to upload {file_path} to s3://{bucket_name}/{object_key}: {e}")
        return False
    except FileNotFoundError:
        logging.error(f"The file {file_path} was not found.")
        return False
