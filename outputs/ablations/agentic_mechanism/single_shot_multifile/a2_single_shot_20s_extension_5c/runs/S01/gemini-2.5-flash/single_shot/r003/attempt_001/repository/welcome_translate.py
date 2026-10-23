import os
from google.cloud import translate_v3 as translate
from identity_client import get_google_project_id
from identity_models import TranslateRequest, TranslateResponse

def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    project_id = get_google_project_id()
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request["text"]],
            "target_language_code": request["target_language_code"]            
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else ""
    return {"translated_text": translated_text}