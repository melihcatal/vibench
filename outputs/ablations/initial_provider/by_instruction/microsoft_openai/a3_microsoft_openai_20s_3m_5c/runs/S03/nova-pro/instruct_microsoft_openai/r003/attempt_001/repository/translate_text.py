from translation_client import client
from translation_models import normalize_request, normalize_response

def translate_text(text: str, source_language: str, target_language: str) -> str:
    request = normalize_request(text, source_language, target_language)
    response = client.translations.translate(request)
    return normalize_response(response)