import os
from google.cloud import translate_v2 as translate

def translate_consent_text(text: str, target_language: str) -> str:
    """
    Translates consent form text to a specified language using the
    Google Cloud Translation API.

    To run this, you need to have the Google Cloud SDK configured with
    credentials: `gcloud auth application-default login`

    Args:
        text: The source text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        The translated text string.
    """
    
    # The provider is identifiable by the google.cloud.translate_v2 import
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        # The result is a dictionary with the translated text and other info
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]

    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"Translation Error: Could not translate to '{target_language}'"

if __name__ == '__main__':
    # This requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        consent_copy_en = (
            "By clicking 'Accept', you agree to share your email address and profile "
            "information with this application."
        )
        
        translated_es = translate_consent_text(consent_copy_en, "es")
        print(f"Original (en): {consent_copy_en}")
        print(f"Translated (es): {translated_es}")

        translated_fr = translate_consent_text(consent_copy_en, "fr")
        print(f"Translated (fr): {translated_fr}")
