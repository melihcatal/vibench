from translation_client import get_translate_client
from translation_models import TranslationResponse

def translate_dictionary_values(input_dict: dict, target_language: str, source_language: str = None) -> dict:
    client = get_translate_client()
    parent = f"projects/{{YOUR_PROJECT_ID}}/locations/global"

    translated_dict = {}
    texts_to_translate = []
    original_keys = []

    for key, value in input_dict.items():
        if isinstance(value, str):
            texts_to_translate.append(value)
            original_keys.append(key)
            translated_dict[key] = None # Placeholder
        else:
            translated_dict[key] = value # Preserve non-string values

    if not texts_to_translate:
        return input_dict

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": texts_to_translate,
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": texts_to_translate,
                "target_language_code": target_language,
            }
        )

    for i, translation in enumerate(response.translations):
        original_key = original_keys[i]
        translated_dict[original_key] = translation.translated_text

    return translated_dict
