import boto3
import os
from botocore.exceptions import NoCredentialsError

def save_audio_to_s3(audio_bytes: bytes, bucket_name: str, object_name: str) -> bool:
    """
    Saves synthesized audio bytes to an AWS S3 bucket.

    Args:
        audio_bytes: The audio data.
        bucket_name: The target S3 bucket.
        object_name: The key for the new object in the bucket.

    Returns:
        True if upload was successful, False otherwise.
    """
    # AWS credentials should be configured in the environment (e.g., via AWS_ACCESS_KEY_ID)
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=audio_bytes,
            ContentType='audio/mpeg'
        )
        return True
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def save_audio_to_local_file(audio_bytes: bytes, file_path: str) -> None:
    """
    Saves synthesized audio bytes to a local file.
    
    Args:
        audio_bytes: The audio data.
        file_path: The local path to save the file.
    """
    with open(file_path, "wb") as out:
        out.write(audio_bytes)

