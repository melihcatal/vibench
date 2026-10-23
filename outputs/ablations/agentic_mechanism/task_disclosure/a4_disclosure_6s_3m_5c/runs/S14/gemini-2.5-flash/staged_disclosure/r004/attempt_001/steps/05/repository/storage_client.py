import os
import boto3
from botocore.exceptions import NoCredentialsError

def get_s3_client():
    """
    Provides a configured AWS S3 client.
    Configuration is loaded from environment variables.
    """
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        return s3_client
    except NoCredentialsError:
        print("AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        return None

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    s3_client = get_s3_client()
    if s3_client is None:
        return False

    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def download_file_from_s3(bucket_name, object_name, file_name):
    """Download a file from an S3 bucket

    :param bucket_name: Bucket to download from
    :param object_name: S3 object name
    :param file_name: Local file name to save as
    :return: True if file was downloaded, else False
    """
    s3_client = get_s3_client()
    if s3_client is None:
        return False

    try:
        s3_client.download_file(bucket_name, object_name, file_name)
        print(f"File {object_name} downloaded to {file_name}")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
