import os
from botocore.exceptions import ClientError

from storage_client import get_storage_client

def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expiration_seconds: int = 3600
) -> str | None:
    """
    Generates a presigned URL to download an object from an S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key of the object.
        expiration_seconds: Time in seconds for the URL to remain valid.

    Returns:
        The presigned URL as a string, or None if an error occurred.
    """
    s3_client = get_storage_client()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_seconds
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL for s3://{bucket_name}/{object_key}: {e}")
        return None

# Example usage (requires environment variables to be set)
# if __name__ == '__main__':
#     BUCKET = os.environ.get("AWS_S3_BUCKET")
#     OBJECT_KEY = "test-upload.txt" # Assuming this object exists
#     if BUCKET:
#         url = create_presigned_download_url(BUCKET, OBJECT_KEY)
#         if url:
#             print(f"Generated presigned URL (valid for 1 hour):\n{url}")
#     else:
#         print("AWS_S3_BUCKET environment variable not set.")
