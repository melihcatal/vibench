from translation_client import TranslationClient
from translation_models import TranslationRequest, normalize_text


def translate_text(text: str, source_language: str, target_language: str) -> str:
    client = TranslationClient()
    request = TranslationRequest(text=normalize_text(text), source_language=source_language, target_language=target_language)
    response = client.post('/translate', params={'api-version': '3.0', 'from': request.source_language, 'to': request.target_language}, json=[{'Text': request.text}])
    response.raise_for_status()
    return response.json()[0]['translations'][0]['text']
