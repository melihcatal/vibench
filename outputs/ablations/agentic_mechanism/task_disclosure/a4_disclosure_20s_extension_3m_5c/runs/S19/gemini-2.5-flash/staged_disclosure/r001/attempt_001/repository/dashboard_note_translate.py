from google.cloud import translate_v2 as translate

def translate_note(text: str, target_language: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud Project ID.

    Returns:
        The translated text.
    """
    translate_client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
