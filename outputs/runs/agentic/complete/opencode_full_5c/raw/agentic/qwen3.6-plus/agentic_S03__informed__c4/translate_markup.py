from translation_client import translate_markup as _translate_markup_client
from translation_models import MarkupTranslationRequest, TranslationResponse


def translate_markup(
    markup_text: str,
    source_language: str,
    target_language: str,
    tag_handling: str = "xml",
    ignore_tags: list[str] | None = None,
) -> TranslationResponse:
    request = MarkupTranslationRequest(
        markup_text=markup_text,
        source_language=source_language,
        target_language=target_language,
        tag_handling=tag_handling,
        ignore_tags=ignore_tags,
    )
    result = _translate_markup_client(
        markup_text=request.markup_text,
        source_language=request.source_language,
        target_language=request.target_language,
        tag_handling=request.tag_handling,
        ignore_tags=request.ignore_tags,
        preserve_formatting=request.preserve_formatting,
    )
    return result
