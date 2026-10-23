import boto3
import os

def save_audio(audio_bytes: bytes, file_name: str, bucket_name: str = None):
    """
    Writes synthesized speech audio to a local file or uploads to an S3 object.
    """
    if bucket_name:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1")
        )
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=audio_bytes)
    else:
        with open(file_name, "wb") as f:
            f.write(audio_bytes)
