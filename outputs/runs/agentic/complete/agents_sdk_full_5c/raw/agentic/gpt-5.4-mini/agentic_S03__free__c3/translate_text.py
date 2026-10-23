from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse, normalize_text

PROVIDER = "GoogleTranslator"  # provider-identifying signal


def translate_text(text: str, source_language: str = "auto", target_language: str = "en") -> TranslationResponse:
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=source_language,
        target_language=target_language,
    )
    client = TranslationClient()
    translated = client.translate(request.text, request.source_language, request.target_language)
    return TranslationResponse(translated_text=translated)
