from translation_client import get_translation_client, get_project_id
from google.cloud import translate_v3beta1

def translate_dictionary_values(input_dict: dict, target_language_code: str, source_language_code: str = None) -> dict:
    client = get_translation_client()
    project_id = get_project_id()
    parent = f"projects/{project_id}/locations/global"

    translated_dict = {}
    texts_to_translate = list(input_dict.values())
    original_keys = list(input_dict.keys())

    if not texts_to_translate:
        return {}

    response = client.translate_text(
        request={'parent': parent,
                 'contents': texts_to_translate,
                 'target_language_code': target_language_code,
                 'source_language_code': source_language_code,
                 'mime_type': 'text/plain'}
    )

    for i, translation in enumerate(response.translations):
        translated_dict[original_keys[i]] = translation.translated_text

    return translated_dict
