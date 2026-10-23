from typing import Optional, List
from document_client import get_azure_translator_client
from document_models import TranslationResult


def translate_invoice_note(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> TranslationResult:
    translation_client = get_azure_translator_client()

    # The SDK expects a list of InputTextItem objects, even for a single string
    # It will automatically detect source language if not provided.
    request_body = [{"text": text}]

    if source_language:
        response = translation_client.translate(
            content=request_body, to=[target_language], from_language=source_language
        )
    else:
        response = translation_client.translate(
            content=request_body, to=[target_language]
        )

    translated_text = ""
    detected_source_language = None

    if response and len(response) > 0 and response[0].translations:
        translated_text = response[0].translations[0].text
        detected_source_language = (
            response[0].detected_language.language
            if response[0].detected_language
            else None
        )

    return TranslationResult(
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=target_language,
    )
