from typing import Optional

import boto3


def stored_text_translate(text: str, source_language: str, target_language: str, region_name: Optional[str] = None) -> str:
    client = boto3.client('translate', region_name=region_name)
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response['TranslatedText']
