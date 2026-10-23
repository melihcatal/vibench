from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, TranslationResponse


def translate_text(text: str, target_lang: str, source_lang: str = None) -> TranslationResponse:
    client = GoogleTranslationClient()
    request = TranslationRequest(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    return client.translate_text(request)