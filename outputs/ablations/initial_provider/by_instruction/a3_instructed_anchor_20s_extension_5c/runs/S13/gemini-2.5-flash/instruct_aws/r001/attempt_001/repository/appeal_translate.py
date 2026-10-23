from safety_client import GoogleCloudClient
from safety_models import AppealTranslateRequest, AppealTranslateResponse

def translate_appeal_text(request: AppealTranslateRequest) -> AppealTranslateResponse:
    client = GoogleCloudClient()
    translated_text = client.translate_text(request.text, request.target_language)
    return AppealTranslateResponse(translated_text=translated_text)
