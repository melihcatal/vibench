import boto3
import os
from typing import List, Dict, Any

def select_voice(language_code: str | None = None) -> List[Dict[str, Any]]:
    """
    Lists available voices from AWS Polly, optionally filtered by language code.

    Args:
        language_code: Optional; a language code to filter voices (e.g., "en-US").

    Returns:
        A list of dictionaries, each representing an available voice.
    """
    polly_client = boto3.client(
        'polly',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = polly_client.describe_voices(IncludeAdditionalLanguageCodes=True)
    voices = response['Voices']

    if language_code:
        return [voice for voice in voices if voice.get('LanguageCode') == language_code]
    return voices
