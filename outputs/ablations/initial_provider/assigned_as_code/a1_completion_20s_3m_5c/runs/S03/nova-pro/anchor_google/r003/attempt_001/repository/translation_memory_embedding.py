from google.cloud import translate_v3

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translation_memory_embedding(translations, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    embeddings = []
    for translation in translations:
        request = TranslationRequest(
            text=translation['text'],
            source_language=translation['source_language'],
            target_language=translation['target_language'],
        ).to_dict()
        response = client.translate_text(request=request, parent=parent)
        embeddings.append({
            'text': translation['text'],
            'source_language': translation['source_language'],
            'target_language': translation['target_language'],
            'embedding': response.embedding,
        })
    return embeddings