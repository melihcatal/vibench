import os
from google.cloud import translate
from typing import List, Dict, Any, Optional


def translate_text_payload(
    text_to_translate: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> Optional[str]:
    """Translates customer-facing message payload text using Google Cloud Translation.

    Args:
        text_to_translate: The text content from the message payload to translate.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).
        source_language: The language code of the input text (optional). If not provided,
                         Google Cloud Translation will auto-detect.

    Returns:
        The translated text, or None if translation fails.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    # The GOOGLE_CLOUD_PROJECT environment variable is typically inferred from credentials

    client = translate.TranslationServiceClient()

    parent = f"projects/{client.project_path(os.environ.get('GOOGLE_CLOUD_PROJECT'))}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text_to_translate],
                "target_language_code": target_language,
                "source_language_code": source_language if source_language else None,
            }
        )

        if response.translations:
            translated_text = response.translations[0].translated_text
            print(
                f"Original: '{text_to_translate}', Translated ({target_language}): '{translated_text}'"
            )
            return translated_text
        return None

    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable (e.g., "your-gcp-project-id")
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to a path of your service account key file

    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    example_text = "Hello, how are you today?"
    example_target_lang = "fr"  # French

    print(f"\n--- Translating text to {example_target_lang} ---")
    translated_result = translate_text_payload(
        example_text, target_language=example_target_lang
    )
    if translated_result:
        print(f"Translated text: {translated_result}")
    else:
        print("Translation failed.")

    example_text_spanish = "¿Qué tal tu día?"
    example_target_lang_english = "en"
    print(f"\n--- Translating text from Spanish to {example_target_lang_english} ---")
    translated_result_en = translate_text_payload(
        example_text_spanish,
        target_language=example_target_lang_english,
        source_language="es",
    )
    if translated_result_en:
        print(f"Translated text: {translated_result_en}")
    else:
        print("Translation failed.")
