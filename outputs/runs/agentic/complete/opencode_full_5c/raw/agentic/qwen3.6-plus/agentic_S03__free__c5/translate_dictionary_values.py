from translation_client import (
    get_translation_client,
    get_parent_location,
    GOOGLE_TRANSLATE_MODEL,
)
from translation_models import TranslationRequest, normalize_request, build_response


def translate_dictionary_values(
    data: dict,
    source_language: str = "en",
    target_language: str = "es",
    model: str = GOOGLE_TRANSLATE_MODEL,
) -> dict:
    client = get_translation_client()
    parent = get_parent_location()

    source_lang_code = source_language
    if source_lang_code == "auto":
        source_lang_code = ""

    text_values = []
    key_mapping = []

    for key, value in data.items():
        if isinstance(value, str) and value.strip():
            text_values.append(value)
            key_mapping.append(key)
        else:
            key_mapping.append((key, value))

    translated_dict = {}

    if text_values:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": text_values,
                "mime_type": "text/plain",
                "source_language_code": source_lang_code,
                "target_language_code": target_language,
            }
        )

        for i, key in enumerate(key_mapping):
            if isinstance(key, tuple):
                translated_dict[key[0]] = key[1]
            else:
                translated_dict[key] = response.translations[i].translated_text
    else:
        for item in key_mapping:
            if isinstance(item, tuple):
                translated_dict[item[0]] = item[1]

    return {
        "translated_dict": translated_dict,
        "source_language": source_language,
        "target_language": target_language,
        "translated_keys_count": len(text_values),
        "model": model,
    }
