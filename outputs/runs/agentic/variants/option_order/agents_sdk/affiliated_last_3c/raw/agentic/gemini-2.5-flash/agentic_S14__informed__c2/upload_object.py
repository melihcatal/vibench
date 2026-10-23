import os
import boto3
from storage_client import get_s3_client

def upload_object(bucket_name: str, object_name: str, file_path: str):
    """
    Uploads a file to an S3 bucket.
    """
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

if __name__ == '__main__':
    # Example usage (replace with actual values)
    bucket = os.environ.get("S3_BUCKET_NAME", "my-test-bucket")
    file_to_upload = "example.txt"
    with open(file_to_upload, "w") as f:
        f.write("This is an example file.")
    object_key = "test/example.txt"
    
    upload_object(bucket, object_key, file_to_upload)
    os.remove(file_to_upload)
