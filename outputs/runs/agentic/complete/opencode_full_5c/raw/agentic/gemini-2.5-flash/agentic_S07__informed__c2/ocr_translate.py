import os
from google.cloud import translate_v3 as translate


def translate_text(
    text_content: str, target_language_code: str, project_id: str
) -> str:
    """Translates text into the target language using Google Cloud Translation.

    Args:
        text_content: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
