import os
import boto3


def generate_audio_preview(text: str, output_path: str):
    """
    Generates an MP3 audio preview of translated text using Amazon Polly.

    Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError("AWS credentials are not set in environment variables.")

    polly_client = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    ).client("polly")

    response = polly_client.synthesize_speech(
        VoiceId="Joanna", OutputFormat="mp3", Text=text
    )

    with open(output_path, "wb") as f:
        f.write(response["AudioStream"].read())
