from observability_client import get_translate_client
from observability_models import TranslateRequest, TranslateResponse
from google.cloud.translate_v3beta1.types import TranslateTextRequest

def log_message_translate(request: TranslateRequest) -> TranslateResponse:
    client = get_translate_client(request.project_id)
    location = "global"  # Or a specific region, e.g., "us-central1"
    parent = f"projects/{request.project_id}/locations/{location}"

    translate_request = TranslateTextRequest(
        parent=parent,
        contents=[request.text_content],
        target_language_code=request.target_language,
    )

    response = client.translate_text(request=translate_request)

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslateResponse(translated_text=translated_text)
