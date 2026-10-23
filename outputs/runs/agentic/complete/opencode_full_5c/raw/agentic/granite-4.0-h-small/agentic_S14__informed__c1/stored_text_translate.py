# stored_text_translate.py
# Translate text extracted from a stored document using Amazon Translate (example)

import os
import boto3
from storage_models import ObjectMetadata
from typing import Dict, Any


def translate_text(source_text: str, target_language: str = "es") -> Dict[str, Any]:
    """Translate `source_text` into `target_language` using Amazon Translate."""
    translate = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    try:
        response = translate.translate_text(
            Text=source_text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language,
        )
    except Exception as exc:
        raise RuntimeError(f"Translation failed: {exc}") from exc
    return {
        "translatedText": response["TranslatedText"],
        "sourceLanguage": response["SourceLanguageCode"],
        "targetLanguage": response["TargetLanguageCode"],
    }


# Example usage:
# document_text = \"Hello world!\"
# translated = translate_text(document_text, target_language="fr")
# print(translated)
