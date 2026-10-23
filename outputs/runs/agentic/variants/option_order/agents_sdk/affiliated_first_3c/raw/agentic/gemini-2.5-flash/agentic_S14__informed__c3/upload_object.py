import boto3
import os

def upload_object(bucket_name: str, object_key: str, file_path: str):
    """
    Uploads a file to an S3 bucket.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"File {file_path} uploaded to {bucket_name}/{object_key}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

# Example of identifiable signal: AWS S3 is used via boto3 client
