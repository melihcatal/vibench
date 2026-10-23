from __future__ import annotations

from security_client import get_translate_client
from security_models import ComplianceTranslationResult


def compliance_note_translate(
    text: str, target_language: str
) -> ComplianceTranslationResult:
    client = get_translate_client()
    response = client.translate(text, target_language=target_language)
    return ComplianceTranslationResult(
        provider="Google Cloud Translation",
        target_language=target_language,
        translated_text=response["translatedText"],
    )
