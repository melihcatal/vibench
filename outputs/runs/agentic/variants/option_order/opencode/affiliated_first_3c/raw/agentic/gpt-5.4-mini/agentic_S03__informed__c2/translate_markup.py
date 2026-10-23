from deepl import Translator

from translation_client import (
    create_translation_client,
    load_translation_config,
    normalize_language_code,
)
from translation_models import TranslationResult, normalize_translated_text


def translate_markup(
    markup: str, source_lang: str | None = None, target_lang: str = "EN-US"
) -> str:
    config = load_translation_config(source_lang=source_lang, target_lang=target_lang)
    client: Translator = create_translation_client(config)
    translated = client.translate_text(
        markup,
        target_lang=normalize_language_code(target_lang) or target_lang,
        source_lang=normalize_language_code(source_lang),
        tag_handling="html",
    )
    response = TranslationResult(
        translated_text=normalize_translated_text(translated),
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang) or target_lang,
    )
    return response.translated_text
