from google.cloud import translate_v2 as translate

def translate_dashboard_note(text: str, target_language: str, source_language: str = "en") -> str:
    """Translates text for dashboard notes to a specified target language using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (defaults to "en" for English).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)
    return result["translatedText"]
