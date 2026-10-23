import os
from google.cloud import translate_v3 as translate

def translate_caption(text: str, target_language: str, project_id: str) -> str:
    """Translates a caption text into another language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "es", "fr").
        project_id: The Google Cloud project ID.

    Returns:
        str: The translated text, or the original text if translation fails.
    """
    if not text.strip():
        return ""

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )

        for translation in response.translations:
            return translation.translated_text
    except Exception as e:
        # In a real application, log the error
        print(f"Translation error: {e}")
        return text # Return original text on failure
    return text
