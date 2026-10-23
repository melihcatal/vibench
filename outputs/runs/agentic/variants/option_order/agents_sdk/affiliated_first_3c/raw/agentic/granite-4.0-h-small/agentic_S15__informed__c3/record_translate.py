import os
import json
from google.cloud.translate_v3 import TranslationServiceClient
from google.cloud.translate_v3.types import TranslateTextRequest, LocationId

# -------------------------------------------------
# Provider setup (Google Cloud Translation)
# -------------------------------------------------
CLIENT = TranslationServiceClient()
TRANSLATION_REGION = "global"  # not used for the global endpoint
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def translate_text(target_language_code: str, source_text: str) -> str:
    """
    Translate a user-facing text field using Google Cloud Translation.

    Args:
        target_language_code (str): ISO-639-1 language code, e.g., "es" for Spanish.
        source_text (str): The text to translate.

    Returns:
        str: Translated text.
    """
    if not GOOGLE_APPLICATION_CREDENTIALS:
        raise RuntimeError('Set GOOGLE_APPLICATION_CREDENTIALS environment variable')

    parent = f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/{TRANSLATION_REGION}"
    request = TranslateTextRequest(
        parent=parent,
        contents=[source_text],
        mime_type='text/plain',
        target_language_code=target_language_code,
    )
    response = CLIENT.translate_text(request=request)
    return response.translations[0].translated_text

if __name__ == "__main__":
    # Example usage with environment variables set
    translated = translate_text(
        target_language_code='es',
        source_text='Hello, world!'
    )
    print('Translated:', translated)
