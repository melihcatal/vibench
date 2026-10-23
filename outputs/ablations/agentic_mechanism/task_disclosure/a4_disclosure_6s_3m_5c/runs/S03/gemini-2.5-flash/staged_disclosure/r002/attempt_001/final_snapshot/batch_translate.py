from google.cloud import translate_v3 as translate

def batch_translate_texts(texts: list[str], target_language: str, project_id: str) -> list[str]:
    """Translates a list of texts into the target language while preserving order.
    Args:
        texts: A list of strings to translate.
        target_language: The language to translate the texts to (e.g., "en" for English).
        project_id: The ID of your Google Cloud project.
    Returns:
        A list of translated strings in the same order as the input texts.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language,
        mime_type="text/plain",  # Mime types: "text/plain", "text/html"
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts
