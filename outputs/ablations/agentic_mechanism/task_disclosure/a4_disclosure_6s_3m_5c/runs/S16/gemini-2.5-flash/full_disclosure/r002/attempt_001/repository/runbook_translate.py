from google.cloud import translate_v3 as translate

def translate_runbook_notes(
    project_id: str,
    text: str,
    target_language: str
) -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation API.

    Args:
        project_id: The ID of the Google Cloud project.
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
