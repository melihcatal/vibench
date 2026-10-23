from translation_client import translate_single
from translation_models import TranslationRequest, TranslationResponse


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
    formality: str | None = None,
) -> TranslationResponse:
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    result = translate_single(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
        formality=request.formality,
        tag_handling=request.tag_handling,
        preserve_formatting=request.preserve_formatting,
    )
    return result
