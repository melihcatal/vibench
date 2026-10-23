import boto3
import os

def upload_object(bucket_name: str, object_name: str, file_path: str):
    """
    Uploads a file to an S3 bucket.
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

