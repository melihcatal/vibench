import os
import boto3


def generate_spoken_brief(text):
    client = boto3.client("polly")
    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=os.getenv("AWS_POLLY_VOICE", "Joanna"),
        Engine="neural",
    )
    return response["AudioStream"].read()

