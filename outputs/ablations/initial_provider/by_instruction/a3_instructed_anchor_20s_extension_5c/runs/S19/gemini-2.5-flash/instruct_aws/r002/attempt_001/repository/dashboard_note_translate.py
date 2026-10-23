import os
import boto3
from typing import Dict, Any

def translate_dashboard_note(
    text: str,
    source_language_code: str,
    target_language_code: str,
) -> Dict[str, Any]:
    """
    Translates metric or dashboard notes for another locale using AWS Translate.
    """
    translate_client = boto3.client('translate', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return {
            "original_text": text,
            "translated_text": response.get('TranslatedText'),
            "source_language": response.get('SourceLanguageCode'),
            "target_language": response.get('TargetLanguageCode'),
        }
    except Exception as e:
        return {"error": str(e)}
