import os
from google.cloud import translate_v2 as translate


def get_translate_client():
    """
    Provides a Google Cloud Translation client.
    Authenticates using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return translate.Client()


def translate_stored_text(
    text_content: str,
    target_language: str,
    project_id: str,
    source_language: str = None,
) -> str:
    """
    Translates text extracted from a stored document using Google Cloud Translation.

    Args:
        text_content: The text content to translate.
        target_language: The language to translate the text into (e.g., 'es' for Spanish).
        project_id: Your Google Cloud project ID.
        source_language: Optional. The language of the input text. If not provided,
                         Google Cloud Translation will attempt to detect it.

    Returns:
        The translated text.
    """
    client = get_translate_client()

    result = client.translate(
        text_content,
        target_language=target_language,
        source_language=source_language,
        model="nmt",  # Neural Machine Translation model
        project_id=project_id,
    )

    return result["translatedText"]
