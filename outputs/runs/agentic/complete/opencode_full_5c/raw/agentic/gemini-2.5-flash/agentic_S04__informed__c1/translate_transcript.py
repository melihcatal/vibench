import os
from google.cloud import translate


def translate_transcript_segment(
    text: str, target_language: str, project_id: str
) -> str:
    """Translates a single transcript segment using Google Cloud Translation.

    Args:
        text: The text segment to translate.
        target_language: The ISO-639-1 code of the target language (e.g., "es").
        project_id: Your Google Cloud Project ID.

    Returns:
        The translated text segment.
    """
    client = translate.TranslationServiceClient()

    # The format_method parameter is deprecated, and is no longer necessary.
    # The Translation API will automatically detect the format of your text.
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
