from google.cloud import translate_v3

from translation_client import build_translation_parent, load_translation_config


def translate_dictionary_values(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    parent = build_translation_parent(config)
    keys = list(payload["data"].keys())
    values = [str(payload["data"][key]) for key in keys]
    response = client.translate_text(request={
        "parent": parent,
        "contents": values,
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "data": {key: translation.translated_text for key, translation in zip(keys, response.translations)},
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
