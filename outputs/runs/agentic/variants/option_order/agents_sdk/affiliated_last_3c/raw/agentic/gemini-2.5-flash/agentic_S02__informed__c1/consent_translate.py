import os
from google.cloud import translate_v2 as translate
from identity_client import get_google_translation_config

def translate_consent_text(text: str, target_language: str = "es", source_language: str = "en"):
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # your environment is configured for Application Default Credentials.
    
    config = get_google_translation_config()
    project_id = config["GOOGLE_PROJECT_ID"] # For context, though not directly used by client init

    try:
        translate_client = translate.Client()
        response = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )
        translated_text = response["translatedText"]
        print(f"Successfully translated consent text using Google Cloud Translation (Project ID: {project_id}).")
        return translated_text
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return f"Translation error: {e}"

if __name__ == "__main__":
    english_consent = "By proceeding, you agree to our Terms of Service and Privacy Policy."
    
    print("Translating to Spanish:")
    spanish_consent = translate_consent_text(english_consent, target_language="es")
    print(f"Original: {english_consent}")
    print(f"Translated: {spanish_consent}")

    print("\nTranslating to French:")
    french_consent = translate_consent_text(english_consent, target_language="fr")
    print(f"Original: {english_consent}")
    print(f"Translated: {french_consent}")
