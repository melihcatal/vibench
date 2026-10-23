import boto3
import os

def synthesize_ssml(ssml_text: str, voice_id: str = "Joanna") -> bytes:
    polly_client = boto3.client(
        "polly",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = polly_client.synthesize_speech(
        Text=ssml_text, TextType="ssml", OutputFormat="mp3", VoiceId=voice_id
    )
    return response["AudioStream"].read()
