import boto3
import os
from typing import List, Dict, Any

def select_voice(locale: str = "en-US") -> List[Dict[str, Any]]:
    """
    Lists available voices for a target locale using Amazon Polly.
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    response = polly_client.describe_voices(
        LanguageCode=locale
    )

    return response["Voices"]
