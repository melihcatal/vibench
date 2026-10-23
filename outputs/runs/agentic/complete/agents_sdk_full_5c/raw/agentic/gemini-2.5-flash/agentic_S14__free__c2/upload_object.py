import boto3
from storage_client import get_s3_client
from typing import BinaryIO

def upload_object(bucket_name: str, object_key: str, data: BinaryIO):
    """
    Uploads a file or byte stream to AWS S3 managed object storage.
    """
    s3_client = get_s3_client()
    s3_client.upload_fileobj(data, bucket_name, object_key)
    return {"message": f"Object {object_key} uploaded successfully to bucket {bucket_name}"}

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with actual bucket name and object key for testing.
    # Ensure you have AWS credentials configured.
    # with open("example.txt", "rb") as f:
    #     result = upload_object("your-s3-bucket-name", "example-upload.txt", f)
    #     print(result)
    pass
