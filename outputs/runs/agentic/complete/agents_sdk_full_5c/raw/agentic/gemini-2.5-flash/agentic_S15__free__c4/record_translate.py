import os
from typing import List, Dict, Any, Optional
from google.cloud import translate_v3 as translate

def translate_document_fields(text_content: str, target_language_code: str, project_id: str) -> Optional[str]:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    
    Args:
        text_content: The text content to translate.
        target_language_code: The BCP-47 language code to translate the text into (e.g., 'es' for Spanish).
        project_id: Your Google Cloud Project ID.
        
    Returns:
        The translated text, or None if translation fails.
    """
    if not project_id:
        print("Google Cloud Project ID is required for translation.")
        return None

    client = translate.TranslationServiceClient()
    location = "global"  # Or a specific region if preferred
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text_content],
                "target_language_code": target_language_code,
            }
        )
        
        if response.translations:
            return response.translations[0].translated_text
            
    except Exception as e:
        print(f"Error translating text: {e}")
    return None

if __name__ == "__main__":
    # Example Usage (requires GOOGLE_CLOUD_PROJECT environment variable and authentication)
    # Make sure GOOGLE_APPLICATION_CREDENTIALS points to a service account key file
    # with 'Cloud Translation API User' role.
    google_project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    sample_text_en = "Hello, how are you? This is a test message for translation."
    target_lang_es = "es"
    target_lang_fr = "fr"
    
    if not google_project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        print(f"Translating text to {target_lang_es}...")
        translated_text_es = translate_document_fields(sample_text_en, target_lang_es, google_project_id)
        if translated_text_es:
            print(f"Original (EN): {sample_text_en}")
            print(f"Translated (ES): {translated_text_es}")
        else:
            print("Failed to translate to Spanish.")
            
        print(f"\nTranslating text to {target_lang_fr}...")
        translated_text_fr = translate_document_fields(sample_text_en, target_lang_fr, google_project_id)
        if translated_text_fr:
            print(f"Original (EN): {sample_text_en}")
            print(f"Translated (FR): {translated_text_fr}")
        else:
            print("Failed to translate to French.")
