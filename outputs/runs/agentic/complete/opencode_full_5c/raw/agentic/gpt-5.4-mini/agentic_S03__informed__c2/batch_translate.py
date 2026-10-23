from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, normalize_texts


def batch_translate(texts, source_language: str, target_language: str):
    client = TranslationClient()
    request = BatchTranslationRequest(texts=normalize_texts(texts), source_language=source_language, target_language=target_language)
    payload = [{'Text': text} for text in request.texts]
    response = client.post('/translate', params={'api-version': '3.0', 'from': request.source_language, 'to': request.target_language}, json=payload)
    response.raise_for_status()
    translated = response.json()
    return [item['translations'][0]['text'] for item in translated]
