import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str = "es") -> str:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.
    Defaults to translating to Spanish.
    """
    client = translate.Client()

    try:
        # Text can also be a list of strings, in which case a list of translations is returned.
        # In this case, we're just translating a single string.
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation API: {e}")
        raise

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    english_consent_copy = (
        "By clicking 'Accept', you agree to our Terms of Service and Privacy Policy. "
        "We will use your profile information to personalize your experience."
    )
    
    print("Translating consent copy to Spanish...")
    try:
        spanish_copy = translate_consent_copy(english_consent_copy, target_language="es")
        print("Original (English):")
        print(english_consent_copy)
        print("\nTranslated (Spanish):")
        print(spanish_copy)
    except Exception as e:
        print(f"Failed to translate consent copy: {e}")
        print("Ensure 'GOOGLE_APPLICATION_CREDENTIALS' environment variable is set and points to your service account key file.")

    print("\nTranslating consent copy to French...")
    try:
        french_copy = translate_consent_copy(english_consent_copy, target_language="fr")
        print("Original (English):")
        print(english_consent_copy)
        print("\nTranslated (French):")
        print(french_copy)
    except Exception as e:
        print(f"Failed to translate consent copy: {e}")
        print("Ensure 'GOOGLE_APPLICATION_CREDENTIALS' environment variable is set and points to your service account key file.")
