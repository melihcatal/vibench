from google.cloud import translate_v2 as translate

def translate_note(text: str, target_language: str) -> str:
    """Translates a metric or dashboard note to a target language using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "es" for Spanish, "fr" for French).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
