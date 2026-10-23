import boto3
import os
from typing import Dict, Any
from database_models import Document

def record_translate(document: Document, field_to_translate: str, target_language_code: str = "en") -> Dict[str, Any]:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    translate = boto3.client("translate", region_name=aws_region)

    text_to_translate = str(document.content.get(field_to_translate, ""))

    if not text_to_translate.strip():
        return {"status": "no_content_to_translate", "translated_text": ""}

    # Detect source language automatically
    # If you know the source language, you can pass it directly to avoid detection overhead
    response = translate.translate_text(
        Text=text_to_translate,
        SourceLanguageCode="auto",  # Automatically detect source language
        TargetLanguageCode=target_language_code
    )

    return {
        "status": "translated",
        "original_text": text_to_translate,
        "translated_text": response['TranslatedText'],
        "source_language": response['SourceLanguageCode'],
        "target_language": response['TargetLanguageCode']
    }
