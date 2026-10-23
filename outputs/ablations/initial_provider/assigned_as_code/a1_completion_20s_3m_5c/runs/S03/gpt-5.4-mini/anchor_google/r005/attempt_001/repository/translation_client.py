from google.cloud import translate_v3


def get_translation_client(config=None):
    return translate_v3.TranslationServiceClient()


def get_translation_parent(config=None):
    config = config or {}
    return f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
