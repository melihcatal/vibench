import os
from google.cloud import translate_v3 as translate

def translate_log_message(
    log_message: str,
    target_language_code: str,
    project_id: str = None
) -> str:
    """Translates a log message to a specified target language using Google Cloud Translation.

    Args:
        log_message: The log message to translate.
        target_language_code: The BCP-47 language code to translate the message into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID. If None, it will be inferred from the environment.

    Returns:
        The translated log message.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [log_message],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return log_message
