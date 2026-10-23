import os
from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "en") -> dict:
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "")

    client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        format_="text",
    )

    return {
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get("detectedSourceLanguage", ""),
        "target_language": target_language,
        "original_text": text,
        "model": "nmt",
        "provider": "google_cloud_translation",
    }
