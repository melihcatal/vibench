import os
import boto3
from storage_client import get_s3_client

def create_presigned_download_url(bucket_name: str, object_key: str, expiration_seconds: int = 3600) -> str:
    """
    Generates a presigned URL for downloading an S3 object.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The object key for which to create the URL.
        expiration_seconds (int): The number of seconds the URL is valid for (default: 3600).

    Returns:
        str: The presigned URL, or an empty string if an error occurs.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_seconds
        )
        print(f"Generated presigned URL for s3://{bucket_name}/{object_key}")
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return ""

if __name__ == '__main__':
    # Example usage (replace with your actual bucket and key)
    # Ensure AWS credentials are configured
    _bucket_name = os.environ.get("AWS_S3_BUCKET_NAME", "your-aws-s3-bucket-name")
    _object_key = "example-uploads/test_upload.txt" # Use an existing object

    presigned_url = create_presigned_download_url(_bucket_name, _object_key, 600)
    if presigned_url:
        print(f"Presigned URL: {presigned_url}")
        print("This URL is valid for 10 minutes.")
    else:
        print("Failed to generate presigned URL.")
