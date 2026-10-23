from google.cloud import translate_v3 as translate
import os

def translate_log_message(log_message: str, target_language_code: str, project_id: str) -> str:
    """Translates a log message to the specified target language using Google Cloud Translation.

    Args:
        log_message: The log message to translate.
        target_language_code: The BCP-47 language code to translate the message into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated log message.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [log_message],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
