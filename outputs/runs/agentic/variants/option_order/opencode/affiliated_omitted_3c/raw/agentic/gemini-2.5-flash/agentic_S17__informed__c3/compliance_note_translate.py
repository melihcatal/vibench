import os
import deepl
from security_models import (
    ComplianceNoteTranslateRequest,
    ComplianceNoteTranslateResponse,
)


def translate_compliance_note(
    request: ComplianceNoteTranslateRequest,
) -> ComplianceNoteTranslateResponse:
    """Translates encryption or compliance notes for reviewers using DeepL."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        text=request.text,
        target_lang=request.target_lang,
        source_lang=request.source_lang,
    )

    # DeepL's result object contains the translated text and detected source language
    translated_text = result.text
    detected_source_lang = result.detected_source_lang

    return ComplianceNoteTranslateResponse(
        translated_text=translated_text,
        source_lang=detected_source_lang,
        target_lang=request.target_lang,
    )
