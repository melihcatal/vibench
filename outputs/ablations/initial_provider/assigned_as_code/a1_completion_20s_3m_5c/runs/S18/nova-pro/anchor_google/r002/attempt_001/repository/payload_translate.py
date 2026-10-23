import boto3
import json


def translate_payload(payload: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(
        Text=payload['message'],
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    payload['message'] = result.translatedText
    return payload