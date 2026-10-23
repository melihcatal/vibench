import boto3
from typing import List

def batch_translate(texts: List[str], source_language: str, target_language: str) -> List[str]:
    """
    Translates a list of strings while preserving order using AWS Translate.
    """
    client = boto3.client('translate')
    translated_texts = []
    for text in texts:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_texts.append(response['TranslatedText'])
    return translated_texts
