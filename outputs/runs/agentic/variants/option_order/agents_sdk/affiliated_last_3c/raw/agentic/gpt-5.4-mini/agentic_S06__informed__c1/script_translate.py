from __future__ import annotations

import os

import boto3

from speech_models import TTSRequest


TRANSLATE_REGION = os.getenv("AWS_DEFAULT_REGION", os.getenv("AWS_REGION", "us-east-1"))


def translate_script(text: str, source_lang: str, target_lang: str) -> str:
    client = boto3.client("translate", region_name=TRANSLATE_REGION)
    request = TTSRequest(text=text, locale=target_lang)
    result = client.translate_text(Text=request.normalized_input(), SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result["TranslatedText"]
