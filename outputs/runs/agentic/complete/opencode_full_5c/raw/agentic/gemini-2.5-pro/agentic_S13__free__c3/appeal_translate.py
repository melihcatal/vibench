from safety_client import get_google_translate_client
from safety_models import AppealTranslateRequest, AppealTranslateResponse


def translate_appeal_text(
    request: AppealTranslateRequest,
) -> AppealTranslateResponse:
    client = get_google_translate_client()
    result = client.translate(request.text, target_language=request.target_language)
    return AppealTranslateResponse(translated_text=result["translatedText"])
