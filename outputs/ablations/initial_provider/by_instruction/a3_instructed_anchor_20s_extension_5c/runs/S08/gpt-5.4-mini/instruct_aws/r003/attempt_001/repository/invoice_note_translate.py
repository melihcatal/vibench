from typing import Any, Dict

from google.cloud import translate_v2 as translate


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate.Client()
    translated = client.translate(text, target_language=target_language)
    return {"provider": "google-cloud-translate", "translated_text": translated.get("translatedText"), "detected_source_language": translated.get("detectedSourceLanguage")}
