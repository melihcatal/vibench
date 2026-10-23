import boto3
import os
from typing import List

def batch_translate(texts: List[str], source_language_code: str, target_language_code: str) -> List[str]:
    """
    Translates a list of strings while preserving order using AWS Translate.
    """
    client = boto3.client(
        'translate',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )

    translated_texts = []
    for text in texts:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_texts.append(response['TranslatedText'])
    
    return translated_texts
