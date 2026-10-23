import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str = "es", project_id: str = None) -> str:
    """
    Translates the given text into the target language using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID. If None, it will try to get from GOOGLE_CLOUD_PROJECT environment variable.

    Returns:
        The translated text.
    """
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT or GCP_PROJECT_ID env var not set.")

    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        translated_text = response.translations[0].translated_text
        print(f"Original text: {text[:50]}...")
        print(f"Translated text ({target_language_code}): {translated_text[:50]}...")
        return translated_text
    else:
        raise Exception("Translation failed or no translations returned.")

if __name__ == "__main__":
    try:
        # Example usage: Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT are set
        sample_text = "Hello, how are you today? I hope you are having a wonderful time."
        translated_result = translate_text(sample_text, target_language_code="fr")
        print(f"\nFull Translated Text (French): {translated_result}")

        sample_text_es = "The quick brown fox jumps over the lazy dog."
        translated_result_es = translate_text(sample_text_es, target_language_code="es")
        print(f"\nFull Translated Text (Spanish): {translated_result_es}")

    except Exception as e:
        print(f"Error in translation: {e}")
