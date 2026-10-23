import os
from google.cloud import translate


def runbook_translate(text: str, target_language: str = "en") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language for the translation (e.g., "en", "es", "fr").

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text
