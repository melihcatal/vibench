import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any

def translate_consent_copy(text: str, target_language: str = "es") -> Dict[str, Any]:
    """
    Translates identity-provider consent copy using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set, pointing to a service account key file.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language
        }
    except Exception as e:
        print(f"Error translating consent copy with Google Cloud Translation: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set to the path of your service account key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/google-cloud-key.json"

    consent_english = "By proceeding, you agree to our Terms of Service and Privacy Policy. Your data will be shared with the application."
    
    try:
        print("Attempting to translate to Spanish...")
        translated_es = translate_consent_copy(consent_english, "es")
        print("Spanish Translation:")
        print(f"Original: {translated_es['original_text']}")
        print(f"Translated: {translated_es['translated_text']}")
        print(f"Source: {translated_es['source_language']}, Target: {translated_es['target_language']}")

        print("\nAttempting to translate to French...")
        translated_fr = translate_consent_copy(consent_english, "fr")
        print("French Translation:")
        print(f"Original: {translated_fr['original_text']}")
        print(f"Translated: {translated_fr['translated_text']}")
        print(f"Source: {translated_fr['source_language']}, Target: {translated_fr['target_language']}")

    except ValueError as e:
        print(f"Configuration Error: {e}. Please ensure GOOGLE_APPLICATION_CREDENTIALS is set.")
    except Exception as e:
        print(f"Runtime Error: {e}. Make sure your service account has 'Cloud Translation API User' role.")
