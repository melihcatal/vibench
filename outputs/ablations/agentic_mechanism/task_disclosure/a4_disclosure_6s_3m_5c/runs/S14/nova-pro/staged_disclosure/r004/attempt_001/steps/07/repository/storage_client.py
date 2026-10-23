import os
import boto3

# Environment variables for AWS S3 configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket"""
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f'File {file_name} uploaded to {bucket}/{object_name}')
    except Exception as e:
        print(e)
        return False
    return True

def download_file(file_name, bucket, object_name=None):
    """Download a file from an S3 bucket"""
    if object_name is None:
        object_name = file_name

    try:
        s3_client.download_file(bucket, object_name, file_name)
        print(f'File {object_name} downloaded from {bucket} to {file_name}')
    except Exception as e:
        print(e)
        return False
    return True