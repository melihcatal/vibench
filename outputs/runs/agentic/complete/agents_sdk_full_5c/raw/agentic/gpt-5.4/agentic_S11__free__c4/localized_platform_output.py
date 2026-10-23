from __future__ import annotations

from typing import Optional

from google.cloud import translate_v2 as translate


def localized_platform_output(text: str, target_locale: str, source_locale: Optional[str] = None) -> dict:
    client = translate.Client()
    response = client.translate(
        text,
        target_language=target_locale,
        source_language=source_locale,
        format_="text",
    )
    return {
        "provider": "google_cloud_translate",
        "translated_text": response["translatedText"],
        "detected_source_language": response.get("detectedSourceLanguage"),
        "target_locale": target_locale,
    }
