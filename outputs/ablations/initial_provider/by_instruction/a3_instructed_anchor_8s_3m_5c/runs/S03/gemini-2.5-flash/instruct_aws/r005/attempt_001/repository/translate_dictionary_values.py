import boto3
import os
from typing import Dict, Any

def translate_dictionary_values(data: Dict[str, str], source_language_code: str, target_language_code: str) -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using AWS Translate.
    """
    client = boto3.client(
        'translate',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )

    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            response = client.translate_text(
                Text=value,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code
            )
            translated_data[key] = response['TranslatedText']
        else:
            translated_data[key] = value # Preserve non-string values

    return translated_data
