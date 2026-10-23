import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


def reviewer_brief_audio(
    brief_text: str, output_file: str, voice_id: str = "Joanna"
) -> str:
    """
    Generate spoken briefs for moderation reviewers using Amazon Polly.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        response = polly_client.synthesize_speech(
            Text=brief_text, OutputFormat="mp3", VoiceId=voice_id, Engine="neural"
        )

        if "AudioStream" in response:
            with open(output_file, "wb") as file:
                file.write(response["AudioStream"].read())

            return output_file
        else:
            raise Exception("No audio stream in response")

    except ClientError as e:
        raise Exception(f"Audio synthesis failed: {e}")
