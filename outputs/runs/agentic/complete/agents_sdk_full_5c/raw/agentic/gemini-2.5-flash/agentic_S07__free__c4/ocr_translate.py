import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language_code: str = "en") -> str:
    """Translates text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()

    # The project ID is used to construct the parent resource name.
    # It's recommended to specify a region if you have specific data residency requirements.
    # For global models, "global" is often used for location.
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == '__main__':
    _project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your project ID
    _text_to_translate = "Hola mundo"
    _translated_text = translate_text(_text_to_translate, _project_id, "es")
    print(f"Original: {_text_to_translate}, Translated: {_translated_text}")

    _translated_text_en = translate_text("Bonjour", _project_id, "en")
    print(f"Original: Bonjour, Translated to English: {_translated_text_en}")
