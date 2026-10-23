import os
from google.cloud import translate_v3 as translate

def translate_text_payload(project_id: str, text_to_translate: str, target_language_code: str, 
                           source_language_code: str = "en") -> dict:
    """Translates customer-facing message payload text using Google Cloud Translation API.
    Returns a dictionary containing the translated text and detected source language.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    # The Text-to-text translation API can translate either a single string or a list of strings.
    # For this example, we assume a single string for simplicity.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code, # Optional, auto-detect if not provided
            "target_language_code": target_language_code,
        }
    )

    translated_data = {
        "translated_text": None,
        "detected_source_language": None
    }

    for translation in response.translations:
        translated_data["translated_text"] = translation.translated_text
        # The API usually returns detected language if source_language_code was not specified
        # or if it was specified and the detection confirms it.
        translated_data["detected_source_language"] = translation.detected_language_code
        break # We only process the first translation for a single input string

    return translated_data

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    text = "Hello, how are you today? This is a test message."
    target_lang = "es"
    
    # print(f"Translating text for project {PROJECT_ID}...")
    # translation_result = translate_text_payload(PROJECT_ID, text, target_lang)
    # print(f"Original: \'{text}\'")
    # print(f"Translated ({target_lang}): \'{translation_result.get("translated_text")}\'")
    # print(f"Detected source language: {translation_result.get("detected_source_language")}")

    # text_fr = "Bonjour, comment allez-vous aujourd'hui?"
    # target_lang_en = "en"
    # translation_result_fr = translate_text_payload(PROJECT_ID, text_fr, target_lang_en)
    # print(f"\nOriginal: \'{text_fr}\'")
    # print(f"Translated ({target_lang_en}): \'{translation_result_fr.get("translated_text")}\'")
    # print(f"Detected source language: {translation_result_fr.get("detected_source_language")}")
