import os
from storage_client import get_translate_client


def translate_text_content(payload, config=None):
    config = config or {}
    text_to_translate = payload["text"]
    source_language_code = payload.get("source_language_code", "auto")  # 'auto' for automatic detection
    target_language_code = payload["target_language_code"]

    translate_client = get_translate_client(config.get("region"))

    try:
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return {
            "translated_text": response["TranslatedText"],
            "source_language_code": response["SourceLanguageCode"],
            "target_language_code": response["TargetLanguageCode"]
        }
    except Exception as e:
        raise RuntimeError(f"Error translating text: {e}")
