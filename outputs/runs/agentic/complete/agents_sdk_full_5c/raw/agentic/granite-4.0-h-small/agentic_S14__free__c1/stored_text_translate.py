import os
from typing import Tuple

# Concrete translation provider: AWS Translate (managed service)
import boto3
from botocore.exceptions import ClientError

def translate_text(source_text: str, target_lang: str = 'FR') -> str:
    """Translate extracted text using AWS Translate.",
    """
    translate = boto3.client('translate')
    try:
        response = translate.translate_text(
            Text=source_text,
            SourceLanguageCode='auto',
            TargetLanguageCode=target_lang
        )
        return response['TranslatedText']
    except ClientError as e:
        raise RuntimeError(f"Translate client error: {e}")
