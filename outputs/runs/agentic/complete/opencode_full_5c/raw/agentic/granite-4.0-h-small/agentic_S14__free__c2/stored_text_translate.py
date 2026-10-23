# Translate extracted text from a stored document (AWS Translate provider)
import os
from storage_client import create_s3_client
import boto3

def translate_text(source_lang: str, target_lang: str, text: str) -> str:
    """Translate `text` from `source_lang` to `target_lang`."
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )
    return response['TranslatedText']
