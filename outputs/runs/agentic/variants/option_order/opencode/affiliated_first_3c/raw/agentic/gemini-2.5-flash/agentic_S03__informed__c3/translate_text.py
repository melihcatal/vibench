from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, TranslationResponse


def translate_single_text(
    text: str, target_language: str, source_language: str = None
) -> TranslationResponse:
    client = GoogleTranslationClient()
    request = TranslationRequest(
        text=text, target_language=target_language, source_language=source_language
    )
    response = client.translate(request)
    return response
