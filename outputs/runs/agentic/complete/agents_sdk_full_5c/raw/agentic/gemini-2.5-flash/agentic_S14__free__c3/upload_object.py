import os
import boto3
from storage_client import get_s3_client

def upload_object(bucket_name: str, object_key: str, file_path: str):
    """
    Uploads a file to an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The desired object key in the S3 bucket.
        file_path (str): The path to the file to upload.
    """
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"File '{file_path}' uploaded to s3://{bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == '__main__':
    # Example usage (replace with your actual bucket, key, and file)
    # Ensure AWS credentials are configured (e.g., via environment variables or ~/.aws/credentials)
    # You might also need to create a dummy file for testing: touch test_upload.txt
    _bucket_name = os.environ.get("AWS_S3_BUCKET_NAME", "your-aws-s3-bucket-name")
    _object_key = "example-uploads/test_upload.txt"
    _file_to_upload = "test_upload.txt" # Make sure this file exists in the same directory

    # Create a dummy file for testing if it doesn't exist
    if not os.path.exists(_file_to_upload):
        with open(_file_to_upload, "w") as f:
            f.write("This is a test file for S3 upload.")
        print(f"Created dummy file: {_file_to_upload}")

    upload_object(_bucket_name, _object_key, _file_to_upload)
