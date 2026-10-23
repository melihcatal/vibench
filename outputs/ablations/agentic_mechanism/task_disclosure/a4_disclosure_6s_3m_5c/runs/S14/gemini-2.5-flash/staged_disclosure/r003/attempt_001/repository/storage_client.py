import boto3
import os

def get_s3_client():
    """
    Returns a boto3 S3 client.
    Configuration can be managed via environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    or other boto3 recognized methods.
    """
    # Initialize S3 client. Boto3 automatically uses environment variables or other credential providers.
    s3_client = boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION', 'us-east-1') # Default to us-east-1 if not set
    )
    return s3_client

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """
    Uploads a file to an S3 bucket.
    :param file_name: File to upload
    :param bucket_name: Name of the S3 bucket
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    s3_client = get_s3_client()
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
    return True

def download_file_from_s3(bucket_name, object_name, file_name):
    """
    Downloads a file from an S3 bucket.
    :param bucket_name: Name of the S3 bucket
    :param object_name: S3 object name
    :param file_name: Local file name to save the download to
    :return: True if file was downloaded, else False
    """
    s3_client = get_s3_client()
    try:
        s3_client.download_file(bucket_name, object_name, file_name)
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
    return True
