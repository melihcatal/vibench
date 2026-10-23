from translation_client import create_translation_client, target_language_code
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(source_language: str, target_language: str, text: str) -> TranslationResponse:
    request = TranslationRequest(source_language=source_language, target_language=target_language, text=normalize_text(text))
    client = create_translation_client()
    result = client.translate_text(request.text, source_lang=target_language_code(request.source_language), target_lang=target_language_code(request.target_language))
    return TranslationResponse(translated_text=result.text, detected_source_language=getattr(result, 'detected_source_lang', None))
