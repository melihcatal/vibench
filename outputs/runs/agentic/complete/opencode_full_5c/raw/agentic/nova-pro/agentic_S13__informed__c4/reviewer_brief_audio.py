import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

import boto3

client = boto3.client(
    "polly",
    region_name="us-west-2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def reviewer_brief_audio(text):
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response["AudioStream"].read()
