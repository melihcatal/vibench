from typing import Any, Dict

import boto3

from extract_text import extract_text


def translate_ocr_text(document: Any, target_language_code: str) -> Dict[str, Any]:
    text = extract_text(document).text
    client = boto3.client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return {"source_text": text, "translated_text": response.get("TranslatedText", "")}
