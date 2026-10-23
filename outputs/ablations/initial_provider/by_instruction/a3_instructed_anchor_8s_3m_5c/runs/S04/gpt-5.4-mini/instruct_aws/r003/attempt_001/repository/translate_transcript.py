import os

import boto3


def translate_transcript(text: str, source_language: str = 'en', target_language: str = 'es') -> dict:
    client = boto3.client('translate', region_name=os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1')))
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response
