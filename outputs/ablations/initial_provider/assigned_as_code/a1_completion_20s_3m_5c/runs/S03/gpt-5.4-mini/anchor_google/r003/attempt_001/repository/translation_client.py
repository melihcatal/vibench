import os

from google.cloud import translate_v3


def load_translation_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "location": config.get("location", "global"),
    }


def create_translation_client(config=None):
    return translate_v3.TranslationServiceClient(), load_translation_config(config)


def build_parent(config):
    return f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"


def translate_texts(texts, source_language, target_language, config=None, mime_type="text/plain"):
    client, resolved = create_translation_client(config)
    response = client.translate_text(request={
        "parent": build_parent(resolved),
        "contents": list(texts),
        "mime_type": mime_type,
        "source_language_code": source_language,
        "target_language_code": target_language,
    })
    return [item.translated_text for item in response.translations]
