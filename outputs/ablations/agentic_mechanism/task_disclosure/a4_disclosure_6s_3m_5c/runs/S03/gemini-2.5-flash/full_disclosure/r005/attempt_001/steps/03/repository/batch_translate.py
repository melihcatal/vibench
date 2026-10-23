
from google.cloud import translate_v3beta1 as translate

def batch_translate_text(
    texts: list[str],
    target_language_code: str,
    project_id: str,
    source_language_code: str = None,
) -> list[str]:
    """Translates a list of texts into the target language.

    Args:
        texts: A list of strings to translate.
        target_language_code: The language code to translate the texts into (e.g., "en-US").
        project_id: The Google Cloud project ID.
        source_language_code: The language code of the input text (e.g., "fr").
                              If not specified, the API will attempt to detect the source language.

    Returns:
        A list of translated strings, preserving the original order.
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

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts
