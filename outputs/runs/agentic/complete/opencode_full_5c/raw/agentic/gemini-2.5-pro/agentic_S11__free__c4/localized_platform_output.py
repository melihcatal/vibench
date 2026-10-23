from google.cloud import translate_v2 as translate
from model_client import get_google_cloud_project


def translate_text(text: str, target_language: str) -> str:
    """
    Translates platform model output for another locale using Google Cloud Translate.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'fr', 'de').

    Returns:
        The translated text.
    """
    project_id = get_google_cloud_project()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    try:
        from invoke_platform_model import invoke_model

        # 1. Get output from the platform model
        original_text_response = invoke_model(
            "The quick brown fox jumps over the lazy dog."
        )
        print(f"Original text: {original_text_response.text}")

        # 2. Translate the output to French
        target_locale = "fr"
        translated_text = translate_text(original_text_response.text, target_locale)
        print(f"Translated text ({target_locale}): {translated_text}")

        # 3. Translate the output to German
        target_locale = "de"
        translated_text_de = translate_text(original_text_response.text, target_locale)
        print(f"Translated text ({target_locale}): {translated_text_de}")

    except (ValueError, ImportError) as e:
        print(f"Error during translation: {e}")
