from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, TranslationResponse


def translate_markup_text(
    markup_text: str, target_language: str, source_language: str = None
) -> TranslationResponse:
    client = GoogleTranslationClient()
    request = TranslationRequest(
        text=markup_text,
        target_language=target_language,
        source_language=source_language,
        format="html",  # Specify format as 'html' for markup translation
    )
    response = client.translate(request)
    return response
