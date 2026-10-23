from google.cloud import translate_v3beta1 as translate

def batch_translate_strings(
    strings: list[str], target_language: str, project_id: str
) -> list[str]:
    """Translates a list of strings into the target language while preserving order.

    Args:
        strings: A list of strings to translate.
        target_language: The language to translate the strings to (e.g., "fr" for French).
        project_id: The Google Cloud project ID.

    Returns:
        A list of translated strings in the original order.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=strings,
        target_language_code=target_language,
    )

    translated_strings = [translation.translated_text for translation in response.translations]
    return translated_strings

