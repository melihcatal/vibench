from safety_models import TranslationRequest, TranslationResponse
from safety_client import translate_text_with_gcp


def translate_appeal_text(text: str, target_language: str) -> TranslationResponse:
    request = TranslationRequest(text=text, target_language=target_language)
    response = translate_text_with_gcp(request)
    return response
