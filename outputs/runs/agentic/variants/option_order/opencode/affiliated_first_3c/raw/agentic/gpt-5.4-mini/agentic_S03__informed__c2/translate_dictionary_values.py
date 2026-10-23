from deepl import Translator

from translation_client import (
    create_translation_client,
    load_translation_config,
    normalize_language_code,
)
from translation_models import (
    TranslationResult,
    normalize_dictionary_values,
    normalize_translated_text,
)


def translate_dictionary_values(
    items: dict[str, str], source_lang: str | None = None, target_lang: str = "EN-US"
) -> dict[str, str]:
    config = load_translation_config(source_lang=source_lang, target_lang=target_lang)
    client: Translator = create_translation_client(config)
    translated_items: dict[str, str] = {}
    for key, value in items.items():
        translated = client.translate_text(
            value,
            target_lang=normalize_language_code(target_lang) or target_lang,
            source_lang=normalize_language_code(source_lang),
        )
        translated_items[key] = normalize_translated_text(translated)
    return normalize_dictionary_values(items, translated_items)
