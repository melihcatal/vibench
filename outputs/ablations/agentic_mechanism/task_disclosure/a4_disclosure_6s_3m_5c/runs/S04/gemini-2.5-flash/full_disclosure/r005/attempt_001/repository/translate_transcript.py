import os
from google.cloud import translate

def translate_transcript_segment(
    text: str,
    target_language_code: str,
    project_id: str,
    source_language_code: str = "en",
) -> str:
    """Translates a single transcript segment using Google Cloud Translation.

    Args:
        text: The text segment to translate.
        target_language_code: The language code to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.
        source_language_code: The language code of the input text (defaults to "en").

    Returns:
        The translated text segment.
    """

    client = translate.TranslationServiceClient()

    location = "global"  # You can specify a different region if needed
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    # Assuming a single text segment is passed for translation
    if response.translations:
        return response.translations[0].translated_text
    return ""
