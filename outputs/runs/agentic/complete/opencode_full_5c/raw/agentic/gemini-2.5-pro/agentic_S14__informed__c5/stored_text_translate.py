from google.cloud import translate_v2 as translate


def translate_stored_text(text: str, target_language: str, project_id: str) -> str:
    """
    Translates text using the Google Cloud Translation API.

    :param text: The text to translate.
    :param target_language: The target language code (e.g., 'fr', 'es').
    :param project_id: The Google Cloud project ID.
    :return: The translated text.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
