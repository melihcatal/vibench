import boto3
import os
from typing import List, Dict, Any

def list_voices_aws(language_code: str = None) -> List[Dict[str, Any]]:
    """
    Lists available voices from AWS Polly, optionally filtered by language code.
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
    response = polly_client.describe_voices(LanguageCode=language_code if language_code else "en-US")
    return response["Voices"]

def select_voice_aws(language_code: str, gender: str = None) -> Dict[str, Any]:
    """
    Selects a voice based on language code and optional gender using AWS Polly.
    This is a simplified selection, often you'd have more sophisticated logic.
    """
    voices = list_voices_aws(language_code=language_code)
    for voice in voices:
        if gender and voice.get("Gender", "").lower() == gender.lower():
            return voice
        elif not gender:
            return voice # Return the first voice if no gender specified
    return {}
