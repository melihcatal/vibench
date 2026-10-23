import boto3
import os
from botocore.exceptions import NoCredentialsError

def upload_file_to_s3(file_path: str, bucket_name: str, object_name: str = None):
    """
    Uploads a file to an S3 bucket.
    :param file_path: Path to the file to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name. If not specified then file_path is used.
    :return: True if file was uploaded, else False.
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def upload_bytes_to_s3(byte_stream: bytes, bucket_name: str, object_name: str):
    """
    Uploads a byte stream to an S3 bucket.
    :param byte_stream: The byte stream to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name.
    :return: True if byte stream was uploaded, else False.
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=byte_stream)
        print(f"Byte stream uploaded to {bucket_name}/{object_name}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error uploading byte stream: {e}")
        return False
