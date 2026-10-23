import os
from google.cloud import translate_v3 as translate

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")

def welcome_translate(text, target_language_code):
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or a specific region, e.g., "us-central1"

    parent = f"projects/{PROJECT_ID}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )
        translations = []
        for translation in response.translations:
            translations.append(translation.translated_text)
        return {"translated_text": translations[0], "target_language": target_language_code}
    except Exception as e:
        return {"error": str(e), "message": "Failed to translate text."}
