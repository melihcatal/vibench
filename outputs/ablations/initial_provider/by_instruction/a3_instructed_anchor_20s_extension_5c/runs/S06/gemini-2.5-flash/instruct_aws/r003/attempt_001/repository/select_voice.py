import boto3
import os
from typing import List, Dict

def select_voice(language_code: str = "en-US") -> List[Dict]:
    """
    Lists available voices for a given language code using AWS Polly.
    """
    polly_client = boto3.client(
        "polly",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = polly_client.describe_voices(
        LanguageCode=language_code
    )

    return response["Voices"]
