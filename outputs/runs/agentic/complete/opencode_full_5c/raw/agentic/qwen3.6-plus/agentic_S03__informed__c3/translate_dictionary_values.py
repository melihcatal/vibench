import deepl
from translation_client import get_translation_client
from translation_models import (
    DictionaryTranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_language_code,
)


def translate_dictionary_values(
    dictionary: dict[str, str],
    source_lang: str | None = None,
    target_lang: str = "en",
    formality: str | None = None,
) -> dict[str, str]:
    client: deepl.Translator = get_translation_client()

    norm_source = normalize_language_code(source_lang) if source_lang else None
    norm_target = normalize_language_code(target_lang)

    deepl_kwargs = {
        "preserve_formatting": True,
    }
    if norm_source:
        deepl_kwargs["source_lang"] = norm_source
    if formality:
        deepl_kwargs["formality"] = formality

    values_list = list(dictionary.values())
    keys_list = list(dictionary.keys())

    if not values_list:
        return {}

    results = client.translate_text(
        values_list, target_lang=norm_target, **deepl_kwargs
    )

    translated_dict = {}
    for i, key in enumerate(keys_list):
        translated_dict[key] = results[i].text

    return translated_dict
