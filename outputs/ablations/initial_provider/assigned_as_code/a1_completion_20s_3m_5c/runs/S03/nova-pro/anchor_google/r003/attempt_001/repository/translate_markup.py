from google.cloud import translate_v3

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_markup(markup, source_language, target_language, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    request = TranslationRequest(
        text=markup,
        source_language=source_language,
        target_language=target_language,
        mime_type='text/html',
    ).to_dict()
    response = client.translate_text(request=request, parent=parent)
    return TranslationResponse.from_dict(response).to_dict()