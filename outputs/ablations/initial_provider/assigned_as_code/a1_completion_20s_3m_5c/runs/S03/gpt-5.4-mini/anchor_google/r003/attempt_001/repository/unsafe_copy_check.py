from google.cloud import translate_v3

from translation_client import load_translation_config, build_parent


def unsafe_copy_check(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    response = client.translate_text(request={
        "parent": build_parent(config),
        "contents": [payload["text"]],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "unsafe": "unsafe" in response.translations[0].translated_text.lower(),
        "text": response.translations[0].translated_text,
    }
