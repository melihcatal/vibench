from google.cloud import translate_v3 as translate

def batch_translate_text(
    texts: list,
    project_id: str,
    target_language_code: str,
    source_language_code: str = None,
) -> list:
    """Translates a list of texts into the target language while preserving order.

    Args:
        texts: A list of strings to translate.
        project_id: Your Google Cloud project ID.
        target_language_code: The language code to translate the texts into (e.g., "es" for Spanish).
        source_language_code: The language code of the input texts (e.g., "en" for English).
                              If not specified, the API will attempt to auto-detect the source language.

    Returns:
        A list of translated strings in the same order as the input texts.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)

    return translated_texts

