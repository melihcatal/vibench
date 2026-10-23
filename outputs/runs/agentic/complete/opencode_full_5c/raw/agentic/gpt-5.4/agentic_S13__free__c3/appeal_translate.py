from __future__ import annotations

from typing import Any, Dict

from safety_client import GOOGLE_TRANSLATE_API_URL, default_session, google_api_key


def appeal_translate(
    text: str, target_language: str = "en", source_language: str | None = None
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "q": text,
        "target": target_language,
        "format": "text",
    }
    if source_language:
        payload["source"] = source_language
    response = default_session().post(
        GOOGLE_TRANSLATE_API_URL,
        params={"key": google_api_key()},
        data=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()["data"]["translations"][0]
    return {
        "translated_text": data.get("translatedText", ""),
        "detected_source_language": data.get("detectedSourceLanguage", source_language),
        "provider": "google_cloud_translation",
    }
