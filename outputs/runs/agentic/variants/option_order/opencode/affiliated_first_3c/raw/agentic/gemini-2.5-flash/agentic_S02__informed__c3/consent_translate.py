import os
from google.cloud import translate_v2 as translate
from identity_client import get_google_cloud_credentials


def translate_consent_copy(text: str, target_language: str = "es") -> str:
    # Google Cloud Translation client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other standard authentication methods.
    # The get_google_cloud_credentials() function is a placeholder for explicit check if needed.
    _ = (
        get_google_cloud_credentials()
    )  # Just to trigger potential error if not set and needed elsewhere

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        return f"Error translating text with Google Cloud Translation: {e}"


if __name__ == "__main__":
    # Example usage: translate consent text
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up (e.g., via a service account key file path)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    sample_consent_text = (
        "By logging in, you agree to our Terms of Service and Privacy Policy."
    )
    target_lang = "fr"
    print(f"Translating '{sample_consent_text}' to {target_lang}...")
    translated_text = translate_consent_copy(sample_consent_text, target_lang)
    print("\nTranslated Text:")
    print(translated_text)

    sample_consent_text_es = "Al iniciar sesión, acepta nuestros Términos de servicio y Política de privacidad."
    target_lang_en = "en"
    print(f"\nTranslating '{sample_consent_text_es}' to {target_lang_en}...")
    translated_text_en = translate_consent_copy(sample_consent_text_es, target_lang_en)
    print("\nTranslated Text:")
    print(translated_text_en)
