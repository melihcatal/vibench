import boto3
import os

def save_audio(audio_bytes: bytes, bucket_name: str, object_key: str):
    """
    Writes synthesized speech audio to an Amazon S3 object.

    Args:
        audio_bytes: The audio byte stream to save.
        bucket_name: The name of the S3 bucket.
        object_key: The key (path) for the S3 object.
    """
    s3_client = boto3.client(
        's3',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=audio_bytes,
        ContentType='audio/mpeg' # Assuming mp3, adjust if other format
    )
    print(f"Audio saved to s3://{bucket_name}/{object_key}")
