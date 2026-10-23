import os
from google.cloud import translate

def translate_platform_output(text: str, target_language: str, project_id: str = None) -> dict:
    """
    Translates platform model output for another locale using Google Cloud Translation API.

    Args:
        text (str): The text content to translate.
        target_language (str): The language to translate the text into (e.g., "es" for Spanish).
        project_id (str, optional): The Google Cloud Project ID. If None, it will be inferred from the environment.

    Returns:
        dict: The translation response including translated text and detected source language.
    """
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")

    client = translate.TranslationServiceClient()
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    detected_source_language = ""
    for translation in response.translations:
        translated_text = translation.translated_text
        detected_source_language = translation.detected_language_code
        break # Assuming single text input
    
    return {
        "translated_text": translated_text,
        "detected_source_language": detected_source_language,
        "raw_response": response.to_dict()
    }
