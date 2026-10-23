from translation_client import translate_text_google
from translation_models import TranslationResponse, TranslationRequest, normalize_text


def translate_text(text: str, source_language: str, target_language: str) -> TranslationResponse:
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    result = translate_text_google(request.text, request.source_language, request.target_language)
    return TranslationResponse(translated_text=result.get("translatedText", ""), provider="google", metadata=result)
