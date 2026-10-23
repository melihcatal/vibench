from google.cloud import translate_v3

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(dictionary, source_language, target_language, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    translated_dict = {}
    for key, value in dictionary.items():
        request = TranslationRequest(
            text=value,
            source_language=source_language,
            target_language=target_language,
        ).to_dict()
        response = client.translate_text(request=request, parent=parent)
        translated_dict[key] = TranslationResponse.from_dict(response).translated_text
    return translated_dict