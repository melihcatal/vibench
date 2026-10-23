from google.cloud import translate_v3

from translation_client import get_translation_client


def translate_dictionary_values(dictionary, source_language, target_language, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    translated_dictionary = {}
    for key, value in dictionary.items():
        response = client.translate_text(request={
            "parent": parent,
            "contents": [value],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
       })
        translated_value = response.translations[0].translated_text
        translated_dictionary[key] = translated_value
    return translated_dictionary