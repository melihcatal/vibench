import os
from typing import Dict, Any

from observability_client import GoogleTranslateClient

def translate_dashboard_note(
    text: str,
    target_language: str,
    project_id: str
) -> str:
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es' for Spanish, 'fr' for French).
        project_id: The Google Cloud Project ID.

    Returns:
        The translated text.
    """
    # Google Cloud credentials must be configured (e.g., via GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or gcloud auth application-default login)

    client = GoogleTranslateClient()
    translated_text = client.translate_text(text, target_language, project_id)
    return translated_text

if __name__ == '__main__':
    # Example usage
    project_id_example = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    
    if project_id_example:
        print("Translating dashboard notes...")

        english_note = "CPU usage is spiking due to a new deployment."
        target_lang_spanish = "es"
        target_lang_french = "fr"

        print(f"\nOriginal (English): '{english_note}'")

        try:
            spanish_translation = translate_dashboard_note(english_note, target_lang_spanish, project_id_example)
            print(f"Translated (Spanish): '{spanish_translation}'")
        except Exception as e:
            print(f"Error translating to Spanish: {e}")

        try:
            french_translation = translate_dashboard_note(english_note, target_lang_french, project_id_example)
            print(f"Translated (French): '{french_translation}'")
        except Exception as e:
            print(f"Error translating to French: {e}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable for example usage.")
