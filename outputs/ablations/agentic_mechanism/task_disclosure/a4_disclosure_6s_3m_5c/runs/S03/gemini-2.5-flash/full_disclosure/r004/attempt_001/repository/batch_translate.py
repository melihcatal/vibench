import os
from google.cloud import translate_v3 as translate

def batch_translate_strings(
    strings: list[str],
    source_language: str,
    target_language: str,
    project_id: str = None
) -> list[str]:
    """Translates a list of strings while preserving their order using Google Cloud Translation API.

    Args:
        strings: A list of strings to translate.
        source_language: The language of the input strings (e.g., "en-US").
        target_language: The language to translate the strings into (e.g., "es").
        project_id: The Google Cloud project ID. If not provided, it will be
                    inferred from the environment.

    Returns:
        A list of translated strings in the same order as the input.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=strings,
        source_language_code=source_language,
        target_language_code=target_language,
        mime_type="text/plain",  # Mime types: "text/plain", "text/html"
    )

    translated_strings = [translation.translated_text for translation in response.translations]
    return translated_strings

