import os
from google.cloud import translate_v2 as translate
from identity_models import TranslationResult

def translate_consent_copy(text: str, target_language: str, source_language: str = "en") -> TranslationResult:
    """
    Translates identity-provider consent copy using Google Cloud Translation.

    Args:
        text: The consent text to translate.
        target_language: The target language code (e.g., "es" for Spanish).
        source_language: The source language code (defaults to "en").

    Returns:
        A TranslationResult object containing the translated text and metadata.
    """
    # Google Cloud Translation client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other standard authentication methods.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key.

    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language, source_language=source_language)

    translated_text = result["translatedText"]
    detected_source_language = result.get("detectedSourceLanguage", source_language)

    return TranslationResult(
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=target_language,
        raw_response=result
    )

if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # e.g., os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    consent_english = "By clicking 'Accept', you agree to our terms of service and privacy policy."
    consent_spanish = "Al hacer clic en 'Aceptar', usted acepta nuestros términos de servicio y política de privacidad."

    print(f"\nTranslating: \"{consent_english}\" to Spanish")
    try:
        translation_es = translate_consent_copy(consent_english, "es")
        print(f"  Translated (ES): {translation_es.translated_text}")
        print(f"  Source Lang: {translation_es.source_language}, Target Lang: {translation_es.target_language}")
    except Exception as e:
        print(f"Error translating to Spanish: {e}")

    print(f"\nTranslating: \"{consent_spanish}\" to French (auto-detect source)")
    try:
        translation_fr = translate_consent_copy(consent_spanish, "fr") # Will auto-detect Spanish
        print(f"  Translated (FR): {translation_fr.translated_text}")
        print(f"  Source Lang: {translation_fr.source_language}, Target Lang: {translation_fr.target_language}")
    except Exception as e:
        print(f"Error translating to French: {e}")
