from google.cloud import translate_v2 as translate
import os

def translate_onboarding_copy(text: str, target_language: str) -> dict:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation API.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or that authentication is otherwise handled (e.g., gcloud auth application-default login)

    translate_client = translate.Client()

    try:
        response = translate_client.translate(text, target_language=target_language)
        translated_text = response['translatedText']
        source_language = response['detectedSourceLanguage']
        return {"success": True, "translated_text": translated_text, "source_language": source_language}
    except Exception as e:
        return {"success": False, "message": str(e)}
