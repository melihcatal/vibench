import os
from google.cloud import translate_v3 as translate
from vision_models import TranslationRequest, TranslationResult

def translate_alt_text(request: TranslationRequest) -> TranslationResult:
    client = translate.TranslationServiceClient()

    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
    location = os.environ.get('GOOGLE_CLOUD_LOCATION', 'global') # 'global' for Cloud Translation V3

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    source_language = response.translations[0].detected_language_code

    return TranslationResult(translated_text=translated_text, source_language_code=source_language)