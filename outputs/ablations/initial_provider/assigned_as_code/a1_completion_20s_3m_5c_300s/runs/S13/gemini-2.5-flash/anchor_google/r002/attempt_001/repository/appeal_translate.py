import os
from google.cloud import translate_v2 as translate
from safety_models import AppealTranslateRequest, AppealTranslateResponse

def translate_appeal_text(request: AppealTranslateRequest, config=None) -> AppealTranslateResponse:
    """
    Translates appeal text using Google Cloud Translation API.

    Args:
        request: An AppealTranslateRequest object.
        config: Optional configuration dictionary, may contain 'project_id'.

    Returns:
        An AppealTranslateResponse object with the translated text.
    """
    # For authentication, Google Cloud SDKs typically pick up credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS) or from gcloud config.
    # No explicit API key passed to client in this case.
    translate_client = translate.Client(project=config.get("project_id") if config else None)

    result = translate_client.translate(
        request.text,
        target_language=request.target_language,
        # Google Cloud Translation API identifies the provider.
        # The client object itself is a strong signal.
    )

    detected_language = result.get('detectedSourceLanguage')
    translated_text = result['translatedText']

    return AppealTranslateResponse(
        original_text=request.text,
        translated_text=translated_text,
        detected_language=detected_language
    )
