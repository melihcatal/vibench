from google.cloud import translate_v3beta1 as translate
from typing import List, Optional

def batch_translate(
    project_id: str,
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None
) -> List[str]:
    """Translates a list of text strings using Google Cloud Translation while preserving order.

    Args:
        project_id: The ID of the GCP project.
        texts: A list of texts to translate.
        target_language: The language to translate the text to (e.g., "es").
        source_language: The language of the input text (e.g., "en"). If None,
                         the API will attempt to detect the source language.

    Returns:
        A list of translated texts in the same order as the input.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",
    )

    translated_texts = []
    if response.translations:
        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts
