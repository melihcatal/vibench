from google.cloud import translate_v2 as translate
from typing import Dict, Any

from identity_client import GOOGLE_CLOUD_PROJECT_ID

def translate_consent_copy(text: str, target_language: str = "es", source_language: str = "en") -> Dict[str, Any]:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.

    Args:
        text: The consent text to translate.
        target_language: The BCP-47 language code to translate the text into (e.g., "es" for Spanish).
        source_language: The BCP-47 language code of the input text (e.g., "en" for English).

    Returns:
        A dictionary containing the translated text and detected source language.
    """
    client = translate.Client(project=GOOGLE_CLOUD_PROJECT_ID)

    # The text to be translated can be a string or a list of strings.
    # For a single string, the result is a dictionary.
    # If the source language is not specified, the API will attempt to detect it.
    result = client.translate(text, target_language=target_language, source_language=source_language)

    translation_info = {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "input_text": text,
        "target_language": target_language
    }
    return translation_info

if __name__ == "__main__":
    consent_english = (
        "By proceeding, you agree to our Terms of Service and Privacy Policy. "
        "This allows us to share your basic profile information with the application."
    )

    print(f"\nTranslating English consent copy to Spanish:\n")
    spanish_translation = translate_consent_copy(consent_english, target_language="es")
    print(f"Original (EN): {spanish_english}")
    print(f"Translated (ES): {spanish_translation['translated_text']}")
    print(f"Detected Source Language: {spanish_translation['source_language']}")

    print(f"\nTranslating English consent copy to French:\n")
    french_translation = translate_consent_copy(consent_english, target_language="fr")
    print(f"Original (EN): {consent_english}")
    print(f"Translated (FR): {french_translation['translated_text']}")
    print(f"Detected Source Language: {french_translation['source_language']}")

    korean_consent = "계속 진행하면 서비스 약관 및 개인 정보 보호 정책에 동의하는 것입니다."
    print(f"\nTranslating Korean consent copy to English:\n")
    english_from_korean = translate_consent_copy(korean_consent, target_language="en", source_language="ko")
    print(f"Original (KO): {korean_consent}")
    print(f"Translated (EN): {english_from_korean['translated_text']}")
    print(f"Detected Source Language: {english_from_korean['source_language']}")
