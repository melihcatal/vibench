import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client

def create_presigned_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """
    Generate a presigned URL to share an S3 object
    :param bucket_name: String
    :param object_name: String
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

    return response

if __name__ == '__main__':
    # Example usage (replace with actual values)
    bucket = os.environ.get("S3_BUCKET_NAME", "my-test-bucket")
    object_key = "test/example.txt"
    url = create_presigned_url(bucket, object_key)
    if url:
        print(f"Presigned URL for {object_key}: {url}")
