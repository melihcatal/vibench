import os
from security_client import get_translate_client


def translate_runbook(text: str, source_language: str, target_language: str) -> str:
    """
    Translates secret-rotation runbook notes using Amazon Translate.
    """
    client = get_translate_client()
    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        return response["TranslatedText"]
    except Exception as e:
        raise RuntimeError(
            f"Error translating runbook notes with Amazon Translate: {e}"
        )
