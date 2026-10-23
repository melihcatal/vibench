from google.cloud import translate_v3

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def unsafe_copy_check(translations, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    unsafe_copies = []
    for translation in translations:
        request = TranslationRequest(
            text=translation['text'],
            source_language=translation['source_language'],
            target_language=translation['target_language'],
        ).to_dict()
        response = client.translate_text(request=request, parent=parent)
        if response.unsafe:
            unsafe_copies.append({
                'text': translation['text'],
                'source_language': translation['source_language'],
                'target_language': translation['target_language'],
                'unsafe': True,
            })
    return unsafe_copies