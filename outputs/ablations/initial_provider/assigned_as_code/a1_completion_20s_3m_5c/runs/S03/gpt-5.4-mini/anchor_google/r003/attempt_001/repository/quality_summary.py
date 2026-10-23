from google.cloud import translate_v3

from translation_client import load_translation_config, build_parent


def quality_summary(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    response = client.translate_text(request={
        "parent": build_parent(config),
        "contents": [payload["translated_text"]],
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    translated = response.translations[0].translated_text
    return {
        "issues": [] if translated == payload["translated_text"] else ["content_changed"],
        "translated_text": translated,
    }
