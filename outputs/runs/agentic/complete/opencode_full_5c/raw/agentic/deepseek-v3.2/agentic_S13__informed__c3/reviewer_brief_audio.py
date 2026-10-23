import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


def reviewer_brief_audio(
    brief_text: str, output_path: str, voice_id: str = "Joanna"
) -> Optional[str]:
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not configured")

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
            with open(output_path, "wb") as file:
                file.write(response["AudioStream"].read())
            return output_path

    except ClientError as e:
        print(f"Error generating audio: {e}")
        return None

    return None
