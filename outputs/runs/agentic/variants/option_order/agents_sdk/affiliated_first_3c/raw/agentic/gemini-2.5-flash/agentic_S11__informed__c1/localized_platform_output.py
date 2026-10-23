import os
from google.cloud import translate_v3 as translate
from typing import Dict, Any, List

def translate_text_for_locale(text: str, target_language_code: str, project_id: str = None) -> Dict[str, Any]:
    """Translates platform model output for another locale using Google Cloud Translation."""
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")

    client = translate.TranslationServiceClient()
    location = "global" # For Cloud Translation, 'global' is common
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return {"translated_text": translated_text, "raw_response": response}

if __name__ == '__main__':
    # Example usage (set GOOGLE_CLOUD_PROJECT env var, ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # original_text = "The quick brown fox jumps over the lazy dog."
    # target_lang = "es"
    # translation_result = translate_text_for_locale(original_text, target_lang)
    # print(f"Original: {original_text}")
    # print(f"Translated ({target_lang}): {translation_result.get("translated_text")}")
    pass
