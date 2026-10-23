import os
from google.cloud import translate_v2 as translate

def translate_runbook_notes(text: str, target_language: str = "es") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation.
    
    Args:
        text: The runbook notes text to translate.
        target_language: The target language code (e.g., "es" for Spanish).
        
    Returns:
        The translated text.
    """
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if available in the environment.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key file
    # or that application default credentials are set up.

    client = translate.Client()
    
    # The target_language parameter is required.
    # The source language will be automatically detected.
    result = client.translate(text, target_language=target_language)
    
    return result['translatedText']

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    # runbook_text = "To rotate the database password, first update the secret in Secret Manager, then update the application configuration."
    # translated_text = translate_runbook_notes(runbook_text, target_language="fr")
    # print(f"Original: {runbook_text}")
    # print(f"Translated (French): {translated_text}")
    pass
