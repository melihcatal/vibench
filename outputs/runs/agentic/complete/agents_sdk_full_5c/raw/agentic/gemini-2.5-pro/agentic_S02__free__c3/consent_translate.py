import os
from google.cloud import translate_v2 as translate

def translate_consent_text(text: str, target_language: str) -> str:
    """
    Translates consent screen text using the Google Cloud Translation API.

    Args:
        text: The source text to translate (e.g., in English).
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        The translated text.
    """
    # Instantiates a client.
    # The client uses Application Default Credentials to authenticate.
    # Ensure you have authenticated via `gcloud auth application-default login`
    # and have set the GCP_PROJECT environment variable.
    translate_client = translate.Client()

    # The text to translate.
    # text = "This application will be able to view your profile information and email address."
    
    try:
        # Translates the text into the target language.
        # The target language defaults to the computer's system language.
        translation_result = translate_client.translate(text, target_language=target_language)
        
        translated_text = translation_result["translatedText"]
        detected_source_language = translation_result["detectedSourceLanguage"]
        
        print(f"Original text: '{text}' (detected language: {detected_source_language})")
        print(f"Translated to '{target_language}': '{translated_text}'")
        
        return translated_text

    except Exception as e:
        print(f"An error occurred with the Google Translation API: {e}")
        # In a real app, you might fall back to the original text.
        return text

if __name__ == '__main__':
    # Example Usage
    # 1. Authenticate with gcloud: `gcloud auth application-default login`
    # 2. Set the GOOGLE_CLOUD_PROJECT environment variable to your GCP Project ID.
    
    consent_copy_en = "This application will be able to view your profile information and email address."
    
    print("--- Translating to Spanish ---")
    translate_consent_text(consent_copy_en, "es")
    
    print("\n--- Translating to French ---")
    translate_consent_text(consent_copy_en, "fr")
    
    print("\n--- Translating to German ---")
    translate_consent_text(consent_copy_en, "de")
