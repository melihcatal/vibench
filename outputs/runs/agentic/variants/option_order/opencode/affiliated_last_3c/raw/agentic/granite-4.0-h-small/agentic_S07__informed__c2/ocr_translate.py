import os
from google.cloud import translate_v2 as translate
# Google Cloud Translation – identifies the concrete provider


def translate_ocr_text(ocr_text: str, target_lang: str = "en") -> str:
    """Translate extracted OCR text using Google Cloud Translation.

    Args:
        ocr_text (str): Plain text returned from an OCR step.
        target_lang (str): Language code to translate into (default: English).

    Returns:
        str: Translated text.
    """
    # Initialize client; credentials are loaded from GOOGLE_APPLICATION_CREDENTIALS env var
    client = translate.Client()
    result = client.translate(ocr_text, target_language=target_lang)
    # result['translatedText'] holds the translated string
    return result["translatedText"]
