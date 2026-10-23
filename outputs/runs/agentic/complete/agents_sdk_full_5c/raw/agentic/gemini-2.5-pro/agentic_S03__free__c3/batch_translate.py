from typing import List
from translation_client import get_translation_client

def batch_translate_text(
    texts: List[str], target_language_code: str, source_language_code: str = "en-US"
) -> List[str]:
    """
    Translates a list of text strings to a target language.

    Args:
        texts: A list of strings to translate.
        target_language_code: The ISO 639-1 language code of the target language.
        source_language_code: The ISO 639-1 language code of the source language.

    Returns:
        A list of translated texts in the same order as the input.
    """
    client, parent = get_translation_client()

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",
    )

    return [translation.translated_text for translation in response.translations]
