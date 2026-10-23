from __future__ import annotations

from messaging_client import get_translate_client


def translate_payload_text(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    client = get_translate_client()
    translated = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return {
        "provider": "google-cloud-translate",
        "translated_text": translated["translatedText"],
        "detected_source_language": translated.get(
            "detectedSourceLanguage", source_language
        ),
        "target_language": target_language,
    }
