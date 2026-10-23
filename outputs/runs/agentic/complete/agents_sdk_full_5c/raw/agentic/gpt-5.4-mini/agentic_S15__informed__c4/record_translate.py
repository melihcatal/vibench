from typing import Any, Dict

from google.cloud import translate_v2 as translate


def translate_record_text(text: str, target_language: str, source_language: str = None) -> Dict[str, Any]:
    client = translate.Client()
    translated = client.translate(text, target_language=target_language, source_language=source_language)
    return {"provider": "Google Cloud Translation", "translated": translated.get("translatedText"), "detectedSourceLanguage": translated.get("detectedSourceLanguage")}
