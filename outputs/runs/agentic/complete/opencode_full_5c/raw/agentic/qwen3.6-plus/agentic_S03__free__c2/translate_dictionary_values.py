from typing import Dict, Any
from translation_models import normalize_language_code, normalize_response_text
from translation_client import (
    get_deepl_client,
    build_translation_options,
    DEEPL_API_ENDPOINT,
)


def translate_dictionary_values(
    data: Dict[str, str],
    source_lang: str = "EN",
    target_lang: str = "ES",
) -> Dict[str, str]:
    client = get_deepl_client()
    source_lang = normalize_language_code(source_lang)
    target_lang = normalize_language_code(target_lang)
    options = build_translation_options(
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=True,
    )
    values = list(data.values())
    keys = list(data.keys())
    if not values:
        return {}
    results = client.translate_text(values, **options)
    translated = {}
    for i, key in enumerate(keys):
        translated[key] = normalize_response_text(results[i].text)
    return translated
