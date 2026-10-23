from google.cloud import translate_v2 as translate

def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation API.

    Args:
        text: The runbook notes to translate.
        target_language: The language to translate the notes to (e.g., "en" for English).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

