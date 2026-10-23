import os
from translation_client import get_translation_client

def translate_single_text(
    text: str, target_language: str, source_language: str = ""
) -> str:
    """Translates a single piece of text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., 'es' for Spanish).
        source_language: The language of the input text (e.g., 'en' for English).
                         If not specified, Google will auto-detect.

    Returns:
        The translated text.
    """
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID environment variable not set. "
            "Please set it to your Google Cloud Project ID."
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "source_language_code": source_language if source_language else None,
        }
    )

    # The response will contain a list of translations, we only asked for one.
    for translation in response.translations:
        return translation.translated_text
    return ""
