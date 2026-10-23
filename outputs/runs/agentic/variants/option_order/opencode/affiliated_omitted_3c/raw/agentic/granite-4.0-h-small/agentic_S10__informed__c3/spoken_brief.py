import boto3
import os


def generate_spoken_brief(text: str) -> bytes:
    """Create an audio file (bytes) from model output using Amazon Polly TTS."""
    audio_stream = boto3.client(
        "polly",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    ).synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna",
    )
    return audio_stream["AudioStream"].read()
