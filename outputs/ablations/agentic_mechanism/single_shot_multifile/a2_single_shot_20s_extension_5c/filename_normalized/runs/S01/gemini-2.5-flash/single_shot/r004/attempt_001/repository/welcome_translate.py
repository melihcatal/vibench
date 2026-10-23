import os
from google.cloud import translate_v3 as translate
from identity_models import TranslateRequest
from identity_client import get_google_project_id

def translate_welcome_message(request: TranslateRequest) -> str:
    project_id = get_google_project_id()
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language_code,
        source_language_code=request.source_language_code,
        mime_type="text/plain",
    )

    if response.translations:
        return response.translations[0].translated_text
    return request.text
