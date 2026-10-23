from translation_client import client
from translation_models import normalize_request, normalize_response

def batch_translate(texts: List[str], source_language: str, target_language: str) -> List[str]:
    translated_texts = []
    for text in texts:
        request = normalize_request(text, source_language, target_language)
        response = client.translations.translate(request)
        translated_texts.append(normalize_response(response))
    return translated_texts