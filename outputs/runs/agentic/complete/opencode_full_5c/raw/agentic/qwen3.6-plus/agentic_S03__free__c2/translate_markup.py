from translation_models import (
    TranslationResponse,
    normalize_language_code,
    normalize_response_text,
)
from translation_client import (
    get_deepl_client,
    build_translation_options,
    DEEPL_API_ENDPOINT,
)


def translate_markup(
    text: str, source_lang: str = "EN", target_lang: str = "ES"
) -> TranslationResponse:
    client = get_deepl_client()
    source_lang = normalize_language_code(source_lang)
    target_lang = normalize_language_code(target_lang)
    options = build_translation_options(
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=True,
        tag_handling="xml",
    )
    result = client.translate_text(text, **options)
    return TranslationResponse(
        translated_text=normalize_response_text(result.text),
        source_lang=result.source_lang,
        target_lang=target_lang,
        character_count=len(text),
    )
