
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str) -> str:
    """Translates identity-provider consent copy using Google Cloud Translation API."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    consent_text = "Do you consent to share your information with this application for authentication purposes?"
    target_lang = "es"  # Spanish

    translated_text = translate_consent_copy(consent_text, target_lang)
    print(f"Original English: {consent_text}")
    print(f"Translated ({target_lang}): {translated_text}")
