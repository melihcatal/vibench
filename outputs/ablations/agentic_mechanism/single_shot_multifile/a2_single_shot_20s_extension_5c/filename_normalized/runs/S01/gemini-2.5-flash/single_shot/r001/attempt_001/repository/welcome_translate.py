import os
from google.cloud import translate_v3 as translate
from identity_models import TranslateTextRequest, TranslateTextResponse

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
if not PROJECT_ID:
    raise EnvironmentError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

def translate_onboarding_copy(request: TranslateTextRequest) -> TranslateTextResponse:
    client = translate.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"

    response = client.translate_text(
        request={'parent': parent,
                 'contents': [request.text],
                 'target_language_code': request.target_language_code,
                 'source_language_code': request.source_language_code,
                 'mime_type': 'text/plain'})
    
    translated_text = ""
    detected_language_code = None
    if response.translations:
        translated_text = response.translations[0].translated_text
        if response.translations[0].detected_language_code:
            detected_language_code = response.translations[0].detected_language_code

    return TranslateTextResponse(
        translated_text=translated_text,
        detected_language_code=detected_language_code
    )