import os
from google.cloud import translate_v2 as translate
from identity_models import TranslationResult

# Configure Google Cloud Translation API
# This assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
# or a service account key file is otherwise discoverable by the client.

def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    """Translates identity-provider consent copy using Google Cloud Translation API."""
    translate_client = translate.Client()

    try:
        # Google Cloud Translation automatically detects source language if not provided
        result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )

        translated_text = result["translatedText"]
        detected_source_language = result["detectedSourceLanguage"]

        return TranslationResult(
            translated_text=translated_text,
            source_language=detected_source_language,
            target_language=target_language,
            provider="Google Cloud Translation"
        )

    except Exception as e:
        return TranslationResult(
            translated_text="",
            source_language=source_language or "unknown",
            target_language=target_language,
            provider="Google Cloud Translation",
            # In a real scenario, you'd add an error message here
        )

if __name__ == "__main__":
    # Example usage
    consent_text_en = "By clicking 'Accept', you agree to our terms and conditions."
    consent_text_es = "Al hacer clic en 'Aceptar', usted acepta nuestros términos y condiciones."

    print("Translating English to Spanish:")
    translation_to_es = translate_consent_copy(consent_text_en, target_language="es")
    print(f"Original: {consent_text_en}")
    print(f"Translated: {translation_to_es.translated_text}")
    print(f"Source: {translation_to_es.source_language}, Target: {translation_to_es.target_language}, Provider: {translation_to_es.provider}")

    print("\nTranslating Spanish to English:")
    translation_to_en = translate_consent_copy(consent_text_es, target_language="en")
    print(f"Original: {consent_text_es}")
    print(f"Translated: {translation_to_en.translated_text}")
    print(f"Source: {translation_to_en.source_language}, Target: {translation_to_en.target_language}, Provider: {translation_to_en.provider}")

    # To run this example, ensure you have Google Cloud authentication set up (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # and the 'google-cloud-translate' library installed.
