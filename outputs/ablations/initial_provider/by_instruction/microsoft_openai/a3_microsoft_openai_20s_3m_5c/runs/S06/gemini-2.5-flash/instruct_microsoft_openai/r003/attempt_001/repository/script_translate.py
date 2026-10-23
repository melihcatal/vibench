import os
from google.cloud import translate_v3 as translate
from speech_models import TranslationRequest

def translate_script(request: TranslationRequest) -> str:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={'parent': parent,
                 'contents': [request.text],
                 'mime_type': 'text/plain',
                 'source_language_code': request.source_language,
                 'target_language_code': request.target_language})

    if response.translations:
        return response.translations[0].translated_text
    else:
        raise Exception("Translation failed: No translations returned.")
