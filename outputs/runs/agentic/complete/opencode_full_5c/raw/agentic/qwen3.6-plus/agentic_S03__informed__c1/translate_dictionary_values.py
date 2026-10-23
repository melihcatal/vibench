from typing import Dict
from translation_client import get_deepl_client
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResult,
    normalize_language_code,
)


def translate_dictionary_values(
    data: Dict[str, str],
    source_lang: str = "",
    target_lang: str = "en",
    preserve_keys: bool = True,
) -> DictionaryTranslationResult:
    request = DictionaryTranslationRequest(
        data=data,
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_keys=preserve_keys,
    )

    if not data:
        return DictionaryTranslationResult(
            translated_data={},
            key_mapping={},
        )

    client = get_deepl_client()

    keys = list(data.keys())
    values = [data[k] for k in keys]

    translate_kwargs = {
        "target_lang": normalize_language_code(target_lang),
        "preserve_formatting": True,
    }
    if source_lang:
        translate_kwargs["source_lang"] = normalize_language_code(source_lang)

    results = client.translate_text(values, **translate_kwargs)

    translated_data = {}
    key_mapping = {}

    for i, key in enumerate(keys):
        result = results[i]
        translated_value = result.text if hasattr(result, "text") else str(result)
        translated_data[key] = translated_value
        key_mapping[key] = key

    return DictionaryTranslationResult(
        translated_data=translated_data,
        key_mapping=key_mapping,
    )
