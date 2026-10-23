import boto3
from storage_client import get_s3_client

def create_presigned_download_url(bucket_name: str, object_key: str, expiration_seconds: int = 3600) -> str:
    """
    Creates a time-limited signed download URL for a stored object in AWS S3.
    """
    s3_client = get_s3_client()
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_seconds
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        raise

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with actual bucket name and object key for testing.
    # Ensure you have AWS credentials configured.
    # presigned_url = create_presigned_download_url("your-s3-bucket-name", "example-upload.txt", 300)
    # print(f"Presigned URL: {presigned_url}")
    pass
