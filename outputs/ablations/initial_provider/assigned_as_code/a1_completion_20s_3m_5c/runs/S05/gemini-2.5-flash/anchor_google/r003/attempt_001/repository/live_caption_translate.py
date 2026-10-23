from google.cloud import translate_v2 as translate
from speech_models import TranslationConfig

def translate_caption(text: str, config: TranslationConfig) -> str:
    """Translates a single caption text using Google Cloud Translation."""
    translate_client = translate.Client()

    # Target language must be an ISO 639-1 code
    result = translate_client.translate(text, target_language=config.target_language_code)

    # print(f"Text: {result['input']}")
    # print(f"Translation: {result['translatedText']}")
    # print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result['translatedText']
