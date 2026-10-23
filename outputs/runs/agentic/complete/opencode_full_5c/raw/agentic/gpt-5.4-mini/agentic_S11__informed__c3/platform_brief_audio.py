import os
import boto3


def generate_platform_brief_audio(text: str) -> bytes:
    client = boto3.client(
        "polly",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response["AudioStream"].read()
