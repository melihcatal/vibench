import boto3

from speech_client import get_speech_client


def save_audio(audio_bytes, file_path):
    with open(file_path, "wb") as f:
        f.write(audio_bytes)


def save_audio_to_s3(audio_bytes, bucket_name, object_key):
    client = boto3.client("s3")
    client.put_object(Body=audio_bytes, Bucket=bucket_name, Key=object_key)