import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any


def translate_consent_copy(
    texts: List[str], target_language_code: str = "es"
) -> List[Dict[str, Any]]:
    """Translates identity-provider consent copy using Google Cloud Translation API."""
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other default credential mechanisms.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key file path.

    client = translate.Client()

    translations = []
    for text in texts:
        try:
            result = client.translate(text, target_language=target_language_code)
            translations.append(
                {
                    "original_text": text,
                    "translated_text": result["translatedText"],
                    "detected_source_language": result["detectedSourceLanguage"],
                }
            )
        except Exception as e:
            print(f"Error translating text '{text}': {e}")
            translations.append(
                {
                    "original_text": text,
                    "translated_text": f"Translation failed: {e}",
                    "detected_source_language": None,
                }
            )
    return translations


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    #
    # consent_texts = [
    #     "Do you consent to share your profile information with this application?",
    #     "This application will access your email address and basic profile details."
    # ]
    # target_lang = "fr"
    #
    # try:
    #     translated_copy = translate_consent_copy(consent_texts, target_lang)
    #     for item in translated_copy:
    #         print(f"Original: {item['original_text']}")
    #         print(f"Translated ({target_lang}): {item['translated_text']}")
    #         print(f"Source Language: {item['detected_source_language']}")
    #         print("---")
    # except Exception as e:
    #     print(f"Error: {e}")
    pass  # placeholder to avoid runtime error if __name__ is run without actual env vars
