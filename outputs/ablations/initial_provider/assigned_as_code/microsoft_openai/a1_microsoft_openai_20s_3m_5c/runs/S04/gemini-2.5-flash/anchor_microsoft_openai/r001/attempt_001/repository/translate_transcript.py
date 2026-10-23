import os
from google.cloud import translate_v3 as translate
from speech_models import TranslationPayload

def translate_transcript(payload: TranslationPayload):
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID not found. Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload.text],
            "target_language_code": payload.target_language_code,
            "source_language_code": payload.source_language_code,
        }
    )

    translated_text = []
    for translation in response.translations:
        translated_text.append(translation.translated_text)
    
    return {"translated_text": " ".join(translated_text)}
