import os
import boto3


def platform_brief_audio(text: str) -> bytes:
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    polly = session.client("polly")
    response = polly.synthesize_speech(
        Text=text[:3000], OutputFormat="mp3", VoiceId="Joanna", Engine="neural"
    )
    audio_stream = response["AudioStream"]
    return audio_stream.read()
