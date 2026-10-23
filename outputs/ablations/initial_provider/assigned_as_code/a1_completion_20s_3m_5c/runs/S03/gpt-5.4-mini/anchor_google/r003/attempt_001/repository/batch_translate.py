from google.cloud import translate_v3

from translation_client import load_translation_config, build_parent
from translation_models import normalize_text_list


def batch_translate(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    texts = normalize_text_list(payload["texts"])
    response = client.translate_text(request={
        "parent": build_parent(config),
        "contents": texts,
        "mime_type": "text/plain",
        "source_language_code": payload["source_language"],
        "target_language_code": payload["target_language"],
    })
    return {
        "texts": [item.translated_text for item in response.translations],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
