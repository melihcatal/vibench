from translation_client import get_translate_client
from translation_models import normalize_response

def batch_translate(texts, target_language):
    client = get_translate_client()
    responses = client.translate_batch(texts, target_language=target_language)
    return [normalize_response(resp) for resp in responses]
