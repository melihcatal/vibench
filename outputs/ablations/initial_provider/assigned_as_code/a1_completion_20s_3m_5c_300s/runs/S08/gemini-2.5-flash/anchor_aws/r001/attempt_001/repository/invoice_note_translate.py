from google.cloud import translate
from typing import Dict, Any
from document_client import load_config

def translate_invoice_notes(text: str, target_language_code: str = "en") -> Dict[str, Any]:
    config = load_config()
    project_id = config.get("google_project_id")
    location = config.get("google_translate_location")

    if not all([project_id, location]):
        raise ValueError("Google Cloud project ID or Translate location is not configured.")

    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Google Cloud Translation.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

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
    
    # Assuming single text input, return the first translation
    translated_text = translations[0] if translations else ""

    return {"translated_text": translated_text, "target_language_code": target_language_code}
