from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = TranslationClient()
    translated_text = client.translate_text(
        text=request.text,
        target_language=request.target_language,
        source_language=request.source_language
    )
    return TranslationResponse(translated_text=translated_text)