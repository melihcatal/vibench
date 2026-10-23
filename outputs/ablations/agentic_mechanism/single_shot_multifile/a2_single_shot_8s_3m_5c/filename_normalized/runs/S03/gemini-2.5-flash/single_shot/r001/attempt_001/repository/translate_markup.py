import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse
from google.cloud.translate_v3 import TranslateTextRequest

def translate_html_markup(request: TranslationRequest) -> TranslationResponse:
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    parent = f"projects/{project_id}"

    translation_request = TranslateTextRequest(
        parent=parent,
        contents=[request.text],
        source_language_code=request.source_language,
        target_language_code=request.target_language,
        mime_type="text/html",
    )

    response = client.translate_text(request=translation_request)
    translated_text = response.translations[0].translated_text

    return TranslationResponse(translated_text=translated_text)
