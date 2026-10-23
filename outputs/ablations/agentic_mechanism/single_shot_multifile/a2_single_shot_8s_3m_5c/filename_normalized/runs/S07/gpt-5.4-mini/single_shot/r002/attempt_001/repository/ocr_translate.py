from typing import Optional

import boto3

from document_models import OcrResult


def translate_ocr_text(result: OcrResult, target_language_code: str, source_language_code: Optional[str] = None) -> str:
    translate = boto3.client("translate")
    response = translate.translate_text(Text=result.text, SourceLanguageCode=source_language_code or "auto", TargetLanguageCode=target_language_code)
    return response.get("TranslatedText", "")
