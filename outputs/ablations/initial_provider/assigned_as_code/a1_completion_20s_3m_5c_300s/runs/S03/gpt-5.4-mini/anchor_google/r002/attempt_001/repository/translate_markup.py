from google.cloud import translate_v3

from translation_client import build_translation_parent, load_translation_config


def translate_markup(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    parent = build_translation_parent(config)
    response = client.translate_text(request={
        "parent": parent,
        "contents": [payload["markup"]],
        "mime_type": payload.get("mime_type", "text/html"),
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "markup": response.translations[0].translated_text,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
