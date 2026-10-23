from translation_client import translate_text_content
from translation_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v2 as translate  # Provider-identifying signal


def translate_text(request: TranslationRequest) -> TranslationResponse:
    translated_text = translate_text_content(
        request.text, request.target_language, request.source_language
    )
    return TranslationResponse(translated_text=translated_text)
