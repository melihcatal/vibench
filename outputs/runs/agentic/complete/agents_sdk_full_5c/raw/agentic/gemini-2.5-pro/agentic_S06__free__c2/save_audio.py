import os
import boto3
from botocore.exceptions import NoCredentialsError


def save_audio_to_s3(audio_bytes: bytes, object_name: str) -> str:
    """
    Uploads synthesized audio bytes to an S3 bucket.

    Requires AWS credentials to be configured in the environment
    (e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    and the BUCKET_NAME environment variable.

    Args:
        audio_bytes: The audio data to upload.
        object_name: The desired key (filename) for the object in S3.

    Returns:
        The S3 object URL.
        
    Raises:
        NoCredentialsError: If AWS credentials are not found.
        ValueError: If BUCKET_NAME environment variable is not set.
    """
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")

    s3_client = boto3.client("s3")
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=audio_bytes,
            ContentType="audio/mpeg"
        )
        
        region = s3_client.meta.region_name
        # Construct the URL
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        return url

    except NoCredentialsError:
        print("AWS credentials not found. Please configure them.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
