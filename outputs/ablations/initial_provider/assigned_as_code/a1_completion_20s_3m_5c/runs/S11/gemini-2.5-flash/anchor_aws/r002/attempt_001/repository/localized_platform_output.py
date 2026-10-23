import os
from google.cloud import translate_v2 as translate

def localized_platform_output(text_output: str, target_language: str, project_id: str = None):
    """
    Translates platform model output for another locale using Google Cloud Translation.
    """
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT_ID environment variable.")

    translate_client = translate.Client(project=project_id) # Google Cloud Translation client

    result = translate_client.translate(
        text_output, 
        target_language=target_language
    )

    translated_text = result["translatedText"]
    detected_source_language = result["detectedSourceLanguage"]
    
    return {
        "translated_text": translated_text,
        "detected_source_language": detected_source_language,
        "target_language": target_language,
        "_provider_response": result
    }
