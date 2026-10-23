import os
from typing import Dict, Any

import boto3

from observability_models import TranslatedText

def dashboard_note_translate(payload: Dict[str, Any], config: Dict[str, Any] = None) -> TranslatedText:
    region_name = config.get("region") if config else os.environ.get("AWS_REGION", "us-east-1")
    translate_client = boto3.client("translate", region_name=region_name)

    text_to_translate = payload["text"]
    target_language = payload["target_language"]
    source_language = payload.get("source_language", "auto") # AWS Translate supports auto-detection

    if not text_to_translate:
        return TranslatedText(translated_text="", source_language=source_language, target_language=target_language)

    try:
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return TranslatedText(
            translated_text=response["TranslatedText"],
            source_language=response["SourceLanguageCode"],
            target_language=response["TargetLanguageCode"]
        )
    except Exception as e:
        return TranslatedText(
            translated_text=f"Translation error: {str(e)}",
            source_language=source_language,
            target_language=target_language
        )
