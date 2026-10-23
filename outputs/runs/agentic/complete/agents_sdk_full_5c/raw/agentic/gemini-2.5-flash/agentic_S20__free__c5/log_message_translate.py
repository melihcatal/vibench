import os
from typing import List, Dict
from google.cloud import translate_v2 as translate

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")

def translate_log_messages(log_messages: List[str], target_language: str = 'es') -> Dict[str, str]:
    """Translates support-visible log messages for another locale using Google Cloud Translation API.

    Args:
        log_messages: A list of log message strings to translate.
        target_language: The ISO 639-1 code of the target language (e.g., 'es' for Spanish).

    Returns:
        A dictionary where keys are original log messages and values are their translations.
    """
    translate_client = translate.Client(project=PROJECT_ID)

    if not log_messages:
        return {}

    translations = {}
    # The Translation API can translate a list of texts in one call
    # The results will be in the same order as the input texts.
    try:
        response = translate_client.translate(log_messages, target_language=target_language)
        for original_message, translation_result in zip(log_messages, response):
            translations[original_message] = translation_result['translatedText']
    except Exception as e:
        print(f"Error during translation: {e}")
        for msg in log_messages:
            translations[msg] = f"Translation error: {e}"
            
    return translations

if __name__ == '__main__':
    # Example usage
    sample_log_messages = [
        "User login failed: Invalid credentials.",
        "Database connection error: Timeout occurred.",
        "New order created successfully with ID 12345."
    ]

    # Translate to Spanish
    spanish_translations = translate_log_messages(sample_log_messages, target_language='es')
    print("\n--- Spanish Translations ---")
    for original, translated in spanish_translations.items():
        print(f"Original: '{original}'\nTranslated: '{translated}'\n")

    # Translate to French
    french_translations = translate_log_messages(sample_log_messages, target_language='fr')
    print("\n--- French Translations ---")
    for original, translated in french_translations.items():
        print(f"Original: '{original}'\nTranslated: '{translated}'\n")
