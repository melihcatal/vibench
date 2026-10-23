import os
from google.cloud import translate


def translate_text_field(text: str, target_language_code: str, project_id: str) -> str:
    """Translates user-facing document fields using Google Cloud Translation.

    Args:
        text (str): The text to translate.
        target_language_code (str): The language code to translate the text into (e.g., "es" for Spanish).
        project_id (str): Your Google Cloud project ID.

    Returns:
        str: The translated text.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    client = translate.TranslationServiceClient()
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Can be "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    # The response can contain multiple translations, but we only sent one piece of text
    for translation in response.translations:
        return translation.translated_text
    return ""
