from google.cloud import translate_v3

from translation_client import load_translation_config


def translation_memory_embedding(payload, config=None):
    config = load_translation_config(config)
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.get_supported_languages(request={"parent": parent})
    return {
        "embedding": [len(payload["segment"]), len(response.languages)],
        "segment": payload["segment"],
    }
