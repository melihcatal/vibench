from deepl import Translator

from translation_client import (
    create_translation_client,
    load_translation_config,
    normalize_language_code,
)
from translation_models import (
    TranslationRequest,
    TranslationResult,
    normalize_translated_text,
)


def translate_text(
    text: str, source_lang: str | None = None, target_lang: str = "EN-US"
) -> str:
    config = load_translation_config(source_lang=source_lang, target_lang=target_lang)
    client: Translator = create_translation_client(config)
    request = TranslationRequest(
        text=text,
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang) or target_lang,
    )
    result = client.translate_text(
        request.text, target_lang=request.target_lang, source_lang=request.source_lang
    )
    response = TranslationResult(
        translated_text=normalize_translated_text(result),
        source_lang=request.source_lang,
        target_lang=request.target_lang,
    )
    return response.translated_text
