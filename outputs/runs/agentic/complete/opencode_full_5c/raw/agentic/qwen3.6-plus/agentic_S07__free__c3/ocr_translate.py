from typing import Optional

from document_client import get_deepl_session
from document_models import TranslationResponse

DEEPL_MODEL_ID = "deepl-free-translation-v2"
DEEPL_SUPPORTED_TARGETS = [
    "DE",
    "EN-US",
    "EN-GB",
    "ES",
    "FR",
    "IT",
    "JA",
    "NL",
    "PL",
    "PT-BR",
    "PT-PT",
    "RU",
    "ZH",
]


def translate_ocr_text(
    text: str,
    target_language: str = "EN",
    source_language: Optional[str] = None,
) -> TranslationResponse:
    session = get_deepl_session()

    payload = {
        "text": text,
        "target_lang": target_language.upper(),
    }
    if source_language:
        payload["source_lang"] = source_language.upper()

    response = session.post("", data=payload)
    response.raise_for_status()

    data = response.json()
    translations = data.get("translations", [])

    translated_text = ""
    detected_source = ""

    if translations:
        translated_text = translations[0].get("text", "")
        detected_source = translations[0].get(
            "detected_source_language", source_language or "unknown"
        )

    return TranslationResponse(
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
    )


def translate_ocr_lines(
    lines: list,
    target_language: str = "EN",
) -> list:
    session = get_deepl_session()
    translated_lines = []

    for line in lines:
        line_text = line.text if hasattr(line, "text") else str(line)
        if not line_text.strip():
            continue

        payload = {
            "text": line_text,
            "target_lang": target_language.upper(),
        }

        response = session.post("", data=payload)
        response.raise_for_status()

        data = response.json()
        translations = data.get("translations", [])

        if translations:
            translated_text = translations[0].get("text", "")
            translated_lines.append(translated_text)

    return translated_lines
