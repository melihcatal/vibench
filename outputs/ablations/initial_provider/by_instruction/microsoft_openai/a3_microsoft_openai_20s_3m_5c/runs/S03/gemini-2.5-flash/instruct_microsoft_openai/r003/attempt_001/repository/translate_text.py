from translation_client import OpenAITranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_text(text: str, source_language: str, target_language: str) -> TranslationResponse:
    client = OpenAITranslationClient()
    request = TranslationRequest(text=text, source_language=source_language, target_language=target_language)
    response = client.translate(request)
    return response
