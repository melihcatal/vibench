import os
from google.cloud import translate_v2 as translate

# Provider: Google Cloud Translation
# Task: Translate metric or dashboard notes for another locale

def translate_dashboard_note(note_text: str, target_language: str = "es") -> dict:
    """
    Translates a given text into the target language using Google Cloud Translation API.

    Args:
        note_text: The text string to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        A dictionary containing the original text, translated text, and detected source language.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for this client to work automatically.
    
    try:
        # The TranslateServiceClient is a provider-specific client class.
        translate_client = translate.Client()
    except Exception as e:
        raise RuntimeError(
            "Could not initialize Google Translate client. "
            "Ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly. "
            f"Original error: {e}"
        )

    if isinstance(note_text, bytes):
        note_text = note_text.decode("utf-8")

    # The 'translate' method is a call to the provider's API.
    result = translate_client.translate(note_text, target_language=target_language)

    return {
        "original_text": note_text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }


if __name__ == '__main__':
    # This example requires authentication to be configured, e.g., by running
    # `gcloud auth application-default login` or setting GOOGLE_APPLICATION_CREDENTIALS
    # to point to a service account key file.
    
    try:
        print("Translating dashboard note...")
        dashboard_note = "CPU utilization has been high for the last hour. Investigating potential memory leak."
        
        translation_result = translate_dashboard_note(dashboard_note, target_language="es")
        
        print(f"\nOriginal ('{translation_result['detected_source_language']}'): {translation_result['original_text']}")
        print(f"Translated ('{translation_result['target_language']}'): {translation_result['translated_text']}")

        translation_result_fr = translate_dashboard_note(dashboard_note, target_language="fr")
        print(f"Translated ('{translation_result_fr['target_language']}'): {translation_result_fr['translated_text']}")

    except Exception as e:
        print(f"Skipping example run due to an error: {e}")
