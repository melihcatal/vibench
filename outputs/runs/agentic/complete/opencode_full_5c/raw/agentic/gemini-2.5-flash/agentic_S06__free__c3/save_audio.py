import boto3
from speech_client import get_s3_client
from io import BytesIO


def save_audio_to_s3(audio_content: bytes, bucket_name: str, file_name: str) -> str:
    s3_client = get_s3_client()

    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=audio_content)
        return f"s3://{bucket_name}/{file_name}"
    except Exception as e:
        print(f"Error saving audio to S3: {e}")
        raise


def save_audio_to_file(audio_content: bytes, file_path: str) -> str:
    try:
        with open(file_path, "wb") as f:
            f.write(audio_content)
        return file_path
    except Exception as e:
        print(f"Error saving audio to local file: {e}")
        raise
