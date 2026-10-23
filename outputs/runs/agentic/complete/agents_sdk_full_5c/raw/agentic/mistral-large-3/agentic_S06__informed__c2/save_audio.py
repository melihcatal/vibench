from typing import Union, BinaryIO
import os
import boto3
from botocore.exceptions import NoCredentialsError
from speech_models import SynthesisResponse


def save_audio_locally(response: SynthesisResponse, file_path: str) -> None:
    with open(file_path, "wb") as f:
        for chunk in response.audio_chunks():
            f.write(chunk)


def save_audio_to_s3(response: SynthesisResponse, bucket: str, key: str) -> str:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    audio_bytes = b"".join(response.audio_chunks())
    s3.put_object(Bucket=bucket, Key=key, Body=audio_bytes)
    return f"s3://{bucket}/{key}"