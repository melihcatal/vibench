import os
import boto3
from botocore.exceptions import NoCredentialsError


def save_audio_to_s3(audio_bytes: bytes, bucket_name: str, object_name: str) -> str:
    """
    Saves audio bytes to an AWS S3 bucket.
    Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables to be set.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=audio_bytes)
        s3_url = f"s3://{bucket_name}/{object_name}"
        return s3_url
    except NoCredentialsError:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )
    except Exception as e:
        raise RuntimeError(f"Failed to save audio to S3: {e}")


def save_audio_to_local_file(audio_bytes: bytes, file_path: str):
    """
    Saves audio bytes to a local file.
    """
    try:
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
    except IOError as e:
        raise RuntimeError(f"Failed to save audio to local file: {e}")
