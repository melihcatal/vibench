from translation_client import create_translation_client
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_text(text, source_language=None, target_language="en"):
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=source_language,
        target_language=target_language,
    )
    client = create_translation_client()
    translated = client.translate_text(
        request.text,
        source_lang=request.source_language,
        target_lang=request.target_language,
    )
    return TranslationResult(
        translated_text=translated.text,
        source_language=request.source_language,
        target_language=request.target_language,
        metadata={"provider": "deepl"},
    )
