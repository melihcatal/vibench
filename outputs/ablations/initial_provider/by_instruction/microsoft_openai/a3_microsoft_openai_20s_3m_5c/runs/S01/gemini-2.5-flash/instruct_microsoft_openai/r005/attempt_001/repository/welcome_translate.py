import os
from google.cloud import translate_v2 as translate
from identity_models import TranslateRequest, TranslateResponse

def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    # Google Cloud Translation API requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # pointing to a service account key file.
    # For local development, ensure this environment variable is configured.
    # The client library will automatically pick up the credentials.
    translate_client = translate.Client()

    # Target language must be an ISO 639-1 code.
    # The translate_client.translate method identifies the provider.
    result = translate_client.translate(
        request.text, target_language=request.target_language)

    return TranslateResponse(
        translated_text=result['translatedText']
    )
