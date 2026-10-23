from google.cloud import translate

def batch_translate_strings(
    texts: list[str],
    target_language_code: str,
    project_id: str,
    source_language_code: str = "en",
) -> list[str]:
    """Translates a list of texts into the target language.

    Args:
        texts: A list of strings to translate.
        target_language_code: The language code to translate the texts into (e.g., "es" for Spanish).
        project_id: The ID of the Google Cloud project.
        source_language_code: The language code of the input texts (e.g., "en" for English).

    Returns:
        A list of translated strings, preserving the order of the input texts.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts

