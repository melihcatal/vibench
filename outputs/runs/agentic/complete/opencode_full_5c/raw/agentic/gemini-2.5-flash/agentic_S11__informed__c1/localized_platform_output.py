import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any

def translate_text_google_cloud(text: str, target_language: str, project_id: str) -> Dict[str, Any]:
    """
    Translates text into the target language using Google Cloud Translation.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    translate_client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "original_text": result["input"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }

if __name__ == '__N__':
    # For local testing, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # And set your Google Cloud Project ID
    google_cloud_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not google_cloud_project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable and ensure GOOGLE_APPLICATION_CREDENTIALS is set.")
    else:
        original_text = "Hello, world! This is a test of the Google Cloud Translation API."
        target_lang = "es" # Spanish

        print(f"Original text: '{original_text}'")
        print(f"Translating to {target_lang}...")
        translation_result = translate_text_google_cloud(original_text, target_lang, google_cloud_project_id)
        print(f"Translation Result: {translation_result}")

        original_text_french = "Bonjour le monde! Comment ça va?"
        target_lang_german = "de" # German
        print(f"
Original text: '{original_text_french}'")
        print(f"Translating to {target_lang_german}...")
        translation_result_2 = translate_text_google_cloud(original_text_french, target_lang_german, google_cloud_project_id)
        print(f"Translation Result: {translation_result_2}")
