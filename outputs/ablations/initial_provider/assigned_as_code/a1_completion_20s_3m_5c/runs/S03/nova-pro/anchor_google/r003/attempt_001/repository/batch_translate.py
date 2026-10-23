from google.cloud import translate_v3

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def batch_translate(texts, source_language, target_language, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    requests = [
        TranslationRequest(
            text=text,
            source_language=source_language,
            target_language=target_language,
        ).to_dict()
        for text in texts
    ]
    responses = client.batch_translate_text(requests=requests, parent=parent)
    return [
        TranslationResponse.from_dict(response).to_dict()
        for response in responses.translations
    ]