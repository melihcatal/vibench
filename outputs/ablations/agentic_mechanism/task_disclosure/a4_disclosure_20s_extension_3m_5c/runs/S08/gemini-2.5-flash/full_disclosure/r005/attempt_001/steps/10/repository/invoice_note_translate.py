from google.cloud import translate_v2 as translate

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language: The target language for translation (e.g., "en" for English).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
