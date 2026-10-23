from google.cloud import translate_v3 as translate

def batch_translate_texts(texts: list[str], target_language: str, project_id: str, source_language: str = None) -> list[str]:
    """Translates a list of texts while preserving order.

    Args:
        texts: A list of texts to translate.
        target_language: The language to translate to.
        project_id: Your Google Cloud project ID.
        source_language: The language of the texts. If not specified, auto-detected.

    Returns:
        A list of translated texts in the original order.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",
    )

    return [translation.translated_text for translation in response.translations]
