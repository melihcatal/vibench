import os
import boto3


def generate_audio_brief(text: str, output_path: str):
    """
    Generates a spoken brief from retrieved search results using Amazon Polly.
    """
    polly_client = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    ).client("polly")

    response = polly_client.synthesize_speech(
        VoiceId="Joanna", OutputFormat="mp3", Text=text, Engine="neural"
    )

    with open(output_path, "wb") as file:
        file.write(response["AudioStream"].read())

    return output_path
