import requests
from document_models import TranslationResult
from document_client import (
    DEEPL_API_KEY,
    DEEPL_API_URL,
    validate_deepl_credentials,
    build_deepl_translation_payload,
    parse_deepl_translation_response,
)


def translate_invoice_note(
    note_text: str,
    target_language: str = "EN",
    source_language: str = "",
) -> TranslationResult:
    if not validate_deepl_credentials():
        raise ValueError("DeepL API key not configured. Set DEEPL_API_KEY.")

    payload = build_deepl_translation_payload(
        text=note_text,
        target_lang=target_language,
        source_lang=source_language,
    )

    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    response_data = response.json()
    parsed = parse_deepl_translation_response(response_data)

    return TranslationResult(
        original_text=note_text,
        translated_text=parsed.get("translated_text", ""),
        source_language=parsed.get("detected_source_language", source_language),
        target_language=target_language,
        provider="deepl",
    )


def translate_invoice_notes_batch(
    notes: list[str],
    target_language: str = "EN",
    source_language: str = "",
) -> list[TranslationResult]:
    results = []
    for note in notes:
        result = translate_invoice_note(
            note_text=note,
            target_language=target_language,
            source_language=source_language,
        )
        results.append(result)
    return results


def translate_invoice_descriptions(
    descriptions: list[str],
    target_language: str = "EN",
) -> list[TranslationResult]:
    return translate_invoice_notes_batch(
        notes=descriptions,
        target_language=target_language,
    )


def translate_single_description(
    description: str,
    target_language: str = "EN",
    source_language: str = "",
) -> str:
    result = translate_invoice_note(
        note_text=description,
        target_language=target_language,
        source_language=source_language,
    )
    return result.translated_text
