import boto3
import os
from typing import List, Dict, Any

def select_voice(language_code: str = "en-US") -> List[Dict[str, Any]]:
    """
    Lists or selects voices for a target locale using Amazon Polly.

    Args:
        language_code: The language code to filter voices by (e.g., "en-US").

    Returns:
        A list of dictionaries, each representing an available voice.
    """
    polly_client = boto3.client(
        'polly',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    response = polly_client.describe_voices(
        LanguageCode=language_code,
        IncludeAdditionalLanguageCodes=True
    )
    return response.get('Voices', [])
