import os
import boto3
import io


def generate_spoken_brief(text: str) -> bytes:
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials not set")

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna", Engine="neural"
    )

    if "AudioStream" in response:
        return response["AudioStream"].read()
    else:
        raise ValueError("No audio generated")
