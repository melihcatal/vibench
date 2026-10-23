from google.cloud import translate_v3beta1

def batch_translate_strings(
    project_id: str,
    location: str,
    source_language: str,
    target_language: str,
    strings: list[str],
) -> list[str]:
    """Translates a list of strings while preserving order using Google Cloud Translation API.

    Args:
        project_id: The ID of the Google Cloud project.
        location: The location of the translation service (e.g., "global").
        source_language: The language of the input strings (e.g., "en").
        target_language: The language to translate the strings to (e.g., "es").
        strings: A list of strings to translate.

    Returns:
        A list of translated strings in the same order as the input.
    """
    client = translate_v3beta1.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=strings,
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_strings = [translation.translated_text for translation in response.translations]
    return translated_strings
