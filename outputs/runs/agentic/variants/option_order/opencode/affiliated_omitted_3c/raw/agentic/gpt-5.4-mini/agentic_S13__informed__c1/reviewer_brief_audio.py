import os

import boto3


def reviewer_brief_audio(text: str):
    client = boto3.client("polly", region_name=os.getenv("AWS_REGION", "us-east-1"))
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response["AudioStream"].read()
