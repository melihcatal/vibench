import os
from typing import Optional

from google.cloud import translate_v2 as translate

from messaging_models import TranslationResult, EventMessage, extract_text_from_payload

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
TRANSLATION_MODEL = "nmt"


def translate_message_payload(
    event: EventMessage,
    target_language: str = "en",
    source_language: Optional[str] = None,
    model: str = TRANSLATION_MODEL,
) -> TranslationResult:
    text = extract_text_from_payload(event.payload)

    client = translate.Client()

    translate_params = {
        "q": text,
        "target": target_language,
        "format_": "text",
        "model": model,
    }

    if source_language:
        translate_params["source"] = source_language

    result = client.translate(**translate_params)

    detected_source = result.get("detectedSourceLanguage", source_language or "unknown")
    translated_text = result.get("translatedText", text)

    return TranslationResult(
        message_id=event.event_id,
        original_text=text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        translation_model=model,
    )


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    message_id: str = "",
    model: str = TRANSLATION_MODEL,
) -> TranslationResult:
    event = EventMessage(
        event_id=message_id,
        payload={"text": text},
    )
    return translate_message_payload(
        event,
        target_language=target_language,
        source_language=source_language,
        model=model,
    )


def translate_batch_payloads(
    events: list,
    target_language: str = "en",
    source_language: Optional[str] = None,
    model: str = TRANSLATION_MODEL,
) -> list:
    client = translate.Client()
    texts = [extract_text_from_payload(e.payload) for e in events]

    translate_params = {
        "q": texts,
        "target": target_language,
        "format_": "text",
        "model": model,
    }

    if source_language:
        translate_params["source"] = source_language

    results = client.translate(**translate_params)

    translations = []
    for idx, result in enumerate(results):
        detected_source = result.get(
            "detectedSourceLanguage", source_language or "unknown"
        )
        translations.append(
            TranslationResult(
                message_id=events[idx].event_id,
                original_text=texts[idx],
                translated_text=result.get("translatedText", texts[idx]),
                source_language=detected_source,
                target_language=target_language,
                translation_model=model,
            )
        )

    return translations
