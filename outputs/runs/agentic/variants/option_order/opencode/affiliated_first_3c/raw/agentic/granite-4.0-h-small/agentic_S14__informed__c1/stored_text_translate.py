# stored_text_translate.py
# [LATER-STEP] Translate extracted text using Amazon Translate (SDK example)

import os
import boto3
from storage_models import OCRResult


def translate_text(source_text: str, target_language: str = "es") -> str:
    """Translates source text to the target language using Amazon Translate.
    Args:
        source_text (str): Text to translate.
        target_language (str): ISO language code (default 'es' for Spanish).
    Returns:
        str: Translated text.
    """
    translate = boto3.client("translate")  # Uses credentials from create_s3_client
    response = translate.translate_text(
        Text=source_text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]


# Example usage with OCRResult
# ocr_res = OCRResult(text='Hello world!')
# translation = translate_text(ocr_res.text, target_language='fr')
# print('French:', translation)
