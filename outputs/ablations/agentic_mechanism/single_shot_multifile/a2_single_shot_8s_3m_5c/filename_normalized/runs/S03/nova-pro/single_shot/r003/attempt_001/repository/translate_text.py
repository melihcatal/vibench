from translation_client import get_translate_client
from translation_models import TranslationRequest, normalize_response

def translate_text(text, target_language):
    client = get_translate_client()
    request = TranslationRequest(text, target_language)
    response = client.translate(request.text, target_language=request.target_language)
    return normalize_response(response)
