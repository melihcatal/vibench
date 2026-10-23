from google.cloud import translate_v3beta1

def translate_log_message(
    project_id: str,
    message: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> str:
    """Translates a log message to the target language using Google Cloud Translation.

    Args:
        project_id: The Google Cloud project ID.
        message: The log message to translate.
        target_language_code: The BCP-47 language code to translate the message into.
        source_language_code: The BCP-47 language code of the original message.

    Returns:
        The translated message.
    """
    client = translate_v3beta1.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[message],
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    if response.translations:
        return response.translations[0].translated_text
    return message
