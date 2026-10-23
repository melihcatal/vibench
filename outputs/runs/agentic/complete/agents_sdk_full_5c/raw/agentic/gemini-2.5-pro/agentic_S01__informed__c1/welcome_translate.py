import os
from google.cloud import translate

def translate_welcome_message(text: str, target_language: str) -> str:
    """
    Translates a welcome message into the user's target language using Google Cloud Translation.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code="en-US",
        target_language_code=target_language,
    )

    if not response.translations:
        raise RuntimeError("Translation failed, no translations returned.")
    
    return response.translations[0].translated_text
