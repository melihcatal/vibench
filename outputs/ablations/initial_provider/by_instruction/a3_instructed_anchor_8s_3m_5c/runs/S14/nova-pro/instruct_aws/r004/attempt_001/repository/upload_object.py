import boto3
from storage_client import get_s3_client

def upload_object(file_path, bucket, key):
    s3_client = get_s3_client()
    with open(file_path, 'rb') as data:
        s3_client.upload_fileobj(data, bucket, key)