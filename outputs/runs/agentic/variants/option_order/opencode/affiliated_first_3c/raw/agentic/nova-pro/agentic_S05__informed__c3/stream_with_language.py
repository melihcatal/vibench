import boto3
import os

transcribe_client = boto3.client(
    "transcribe",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def start_stream_with_language(language_code="en-US"):
    response = transcribe_client.start_stream_transcription(
        LanguageCode=language_code,
        MediaEncoding="pcm",
        MediaSampleRateHertz=16000,
        StreamURL="https://your-stream-url",
        EnablePunctuation=True,
        EnableSpeakerIdentification=True,
    )
    return response
