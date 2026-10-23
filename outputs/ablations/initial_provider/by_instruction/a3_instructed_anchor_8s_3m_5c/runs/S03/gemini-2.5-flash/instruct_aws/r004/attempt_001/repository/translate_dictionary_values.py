import boto3
from typing import Dict, Any

def translate_dictionary_values(data: Dict[str, Any], source_language: str, target_language: str) -> Dict[str, Any]:
    """
    Translates dictionary values while preserving keys using AWS Translate.
    """
    client = boto3.client('translate')
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            response = client.translate_text(
                Text=value,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language
            )
            translated_data[key] = response['TranslatedText']
        else:
            translated_data[key] = value # Preserve non-string values
    return translated_data
