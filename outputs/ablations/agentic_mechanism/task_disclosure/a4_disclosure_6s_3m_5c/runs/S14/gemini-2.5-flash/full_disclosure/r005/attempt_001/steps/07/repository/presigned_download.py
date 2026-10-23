import os
import boto3
from botocore.exceptions import NoCredentialsError

def create_presigned_download_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """
    Generates a time-limited presigned URL for downloading a stored object from AWS S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The name of the object in the S3 bucket.
        expiration (int): The number of seconds the presigned URL is valid for (default: 3600 seconds).

    Returns:
        str: The presigned URL if successful, otherwise None.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN")
    )
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
    except NoCredentialsError:
        print("AWS credentials not found. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY environment variables.")
        return None
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None
    return response
