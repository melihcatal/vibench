import os
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def translate_query(query: str, target_lang: str = 'en') -> str:
    """Translate a multilingual query into the target language using Translation API.
    This example uses Google Cloud Translation SDK (provider signal: GOOGLE_APPLICATION_CREDENTIALS).
    """
    from google.cloud import translate_v2 as translate
    client = translate.Client()
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise RuntimeError('GOOGLE_APPLICATION_CREDENTIALS env variable not set')
    result = client.translate(query, target_language=target_lang)
    return result['translatedText']
