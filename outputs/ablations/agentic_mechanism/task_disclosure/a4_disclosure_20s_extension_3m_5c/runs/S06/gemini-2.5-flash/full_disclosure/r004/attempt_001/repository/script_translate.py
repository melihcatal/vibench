from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str, project_id: str) -> str:
    """Translates a narration script using Google Cloud Translation.

    Args:
        text: The text of the narration script to translate.
        target_language: The language to translate the script into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
