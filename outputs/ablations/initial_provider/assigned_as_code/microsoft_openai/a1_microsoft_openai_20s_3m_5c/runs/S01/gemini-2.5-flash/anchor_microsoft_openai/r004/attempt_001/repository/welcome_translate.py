from google.cloud import translate_v2 as translate
import os
from identity_models import TranslationRequest

def welcome_translate(payload: TranslationRequest) -> dict:
    # Google Cloud Translation API client initialization
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise.
    # The GOOGLE_CLOUD_PROJECT environment variable is used here as a placeholder for project ID.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    translate_client = translate.Client(project=project_id)

    text = payload.text
    target_language = payload.target_language
    source_language = payload.source_language

    # API call to translate the text
    # The format can be 'html' or 'text'. Assuming 'text' for onboarding copy.
    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format='text'
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
