from google.cloud import translate_v3 as translate

def translate_log_message(project_id: str, text: str, target_language_code: str, location: str = "global") -> str:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        text (str): The log message text to translate.
        target_language_code (str): The BCP-47 language code of the target language (e.g., "es" for Spanish).
        location (str): The location of the Translation API endpoint (e.g., "global" or "us-central1").

    Returns:
        str: The translated log message.
    """

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return translated_text
