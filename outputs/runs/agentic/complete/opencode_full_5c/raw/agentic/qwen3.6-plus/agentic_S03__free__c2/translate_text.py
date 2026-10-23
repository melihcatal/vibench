from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_language_code,
    normalize_response_text,
)
from translation_client import (
    get_deepl_client,
    build_translation_options,
    DEEPL_API_ENDPOINT,
)


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_deepl_client()
    source_lang = normalize_language_code(request.source_lang)
    target_lang = normalize_language_code(request.target_lang)
    options = build_translation_options(
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=request.preserve_formatting,
        tag_handling=request.tag_handling,
    )
    result = client.translate_text(request.text, **options)
    return TranslationResponse(
        translated_text=normalize_response_text(result.text),
        source_lang=result.source_lang,
        target_lang=target_lang,
        character_count=len(request.text),
    )
