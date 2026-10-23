import os
from typing import List, Dict, Any, Optional
from google.cloud import translate_v2 as translate

def translate_log_message(text: str, target_language_code: str, project_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Translates a support-visible log message to a specified target locale using Google Cloud Translation.

    Args:
        text (str): The log message text to translate.
        target_language_code (str): The BCP-47 language code of the target language (e.g., "es" for Spanish, "fr" for French).
        project_id (Optional[str]): The Google Cloud Project ID. If None, it will be read from GOOGLE_CLOUD_PROJECT env var.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the translated text and source language, or None if an error occurs.
    """
    if not text:
        return {"translated_text": "", "detected_source_language": ""}

    if project_id is None:
        # The translate_v2 client does not strictly require project_id in its constructor
        # if GOOGLE_APPLICATION_CREDENTIALS or default credentials are set up correctly.
        # However, for consistency and explicit identification, we keep the check.
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Translation might rely on default credentials.")

    translate_client = translate.Client(project=project_id)

    try:
        result = translate_client.translate(text, target_language=target_language_code)
        translated_text = result['translatedText']
        detected_source_language = result['detectedSourceLanguage']
        print(f"Successfully translated log message to {target_language_code}.")
        return {
            "translated_text": translated_text,
            "detected_source_language": detected_source_language
        }
    except Exception as e:
        print(f"Error translating log message: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable and ensure translation API is enabled
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    english_message = "Failed to connect to the database. Please check network settings."
    spanish_message = translate_log_message(english_message, "es")
    if spanish_message:
        print("\n--- English to Spanish Translation ---")
        print(f"Original (EN): {english_message}")
        print(f"Translated (ES): {spanish_message['translated_text']}")
        print(f"Detected Source Language: {spanish_message['detected_source_language']}")

    german_message = translate_log_message("User login attempt failed due to invalid password.", "de")
    if german_message:
        print("\n--- English to German Translation ---")
        print(f"Original (EN): User login attempt failed due to invalid password.")
        print(f"Translated (DE): {german_message['translated_text']}")
        print(f"Detected Source Language: {german_message['detected_source_language']}")

    # Example with a non-English source and different target
    french_message = translate_log_message("L'utilisateur a rencontré une erreur interne.", "en")
    if french_message:
        print("\n--- French to English Translation ---")
        print(f"Original (FR): L'utilisateur a rencontré une erreur interne.")
        print(f"Translated (EN): {french_message['translated_text']}")
        print(f"Detected Source Language: {french_message['detected_source_language']}")
