import os
import boto3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def generate_brief_audio(text):
    polly = boto3.client(
        "polly",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    with open("brief.mp3", "wb") as file:
        file.write(response["AudioStream"].read())
