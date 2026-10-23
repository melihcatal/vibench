import boto3
import os

def save_audio(audio_bytes: bytes, bucket_name: str, key: str):
    s3_client = boto3.client(
        "s3",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=audio_bytes)
