from google.cloud import translate_v2 as translate

def localized_platform_output(text: str, target_language: str, project_id: str) -> str:
    """Translates platform model output to another locale using Google Cloud Translation API.

    Args:
        text: The text content to translate.
        target_language: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    translate_client = translate.Client(project=project_id)
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
