import os

import boto3


def platform_brief_audio(text: str):
    client = boto3.client(
        "polly",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    return client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId=os.getenv("POLLY_VOICE_ID", "Joanna")
    )
