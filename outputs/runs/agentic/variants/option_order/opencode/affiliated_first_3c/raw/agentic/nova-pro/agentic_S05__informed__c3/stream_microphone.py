import boto3
import os

transcribe_client = boto3.client(
    "transcribe",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def start_stream():
    response = transcribe_client.start_stream_transcription(
        LanguageCode="en-US",
        MediaEncoding="pcm",
        MediaSampleRateHertz=16000,
        StreamURL="https://your-stream-url",
    )
    return response
