from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str, project_id: str) -> str:
    """
    Translates text to a target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language (e.g., 'es', 'fr').
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
