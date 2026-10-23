from google.cloud import translate_v3


def get_translation_client():
    return translate_v3.TranslationServiceClient()


def get_translation_parent(config):
    config = config or {}
    return f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"


def get_text_mime_type(is_html=False):
    return "text/html" if is_html else "text/plain"
