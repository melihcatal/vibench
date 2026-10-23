from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_text_aws(request: TranslationRequest) -> TranslationResponse:
    client = TranslationClient()
    translated_text = client.translate_text(request.text, request.source_language, request.target_language)
    return TranslationResponse(translated_text, request.source_language, request.target_language)
