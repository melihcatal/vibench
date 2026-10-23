import os
from typing import Dict, Any, Optional
import boto3

def get_boto3_client(service_name: str, region_name: Optional[str] = None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(service_name, region_name=region_name)

def translate_message_text(
    text: str,
    source_language_code: str,
    target_language_code: str,
    region_name: Optional[str] = None
) -> Dict[str, Any]:
    translate_client = get_boto3_client("translate", region_name=region_name)

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return {
            "translated_text": response['TranslatedText'],
            "source_language": response['SourceLanguageCode'],
            "target_language": response['TargetLanguageCode']
        }
    except Exception as e:
        return {"error": str(e), "original_text": text}
