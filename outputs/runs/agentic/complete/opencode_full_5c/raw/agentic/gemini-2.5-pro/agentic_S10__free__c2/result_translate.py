from model_client import get_google_translate_client
from model_models import TranslationRequest, TranslationResponse


def translate_result(request: TranslationRequest) -> TranslationResponse:
    client = get_google_translate_client()

    if not request.text:
        return TranslationResponse(translated_text="", raw_response=None)

    result = client.translate(request.text, target_language=request.target_language)

    return TranslationResponse(
        translated_text=result["translatedText"], raw_response=result
    )
