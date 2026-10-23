from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en" for English).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
