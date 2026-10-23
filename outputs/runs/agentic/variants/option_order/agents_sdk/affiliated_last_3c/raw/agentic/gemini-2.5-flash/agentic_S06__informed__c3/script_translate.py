
import os
from google.cloud import translate_v3 as translate
from speech_client import TranslationClient

def translate_script(text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates narration scripts using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language_code: The language code to translate the text to (e.g., "es").
        source_language_code: The language code of the input text (e.g., "en").

    Returns:
        The translated text.
    """
    client_wrapper = TranslationClient()
    client = client_wrapper.client
    project_id = client_wrapper.project_id

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
