import os
import boto3

# Set up the Amazon Polly client
polly_client = boto3.client(
    "polly",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def reviewer_brief_audio(text):
    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna"
    )
    with open("reviewer_brief.mp3", "wb") as f:
        f.write(response["AudioStream"].read())
