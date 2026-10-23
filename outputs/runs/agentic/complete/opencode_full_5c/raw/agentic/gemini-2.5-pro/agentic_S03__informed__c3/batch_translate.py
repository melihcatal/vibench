from translation_client import get_translation_client


def batch_translate(
    texts: list[str], target_language: str, source_language: str = "en"
):
    """
    Translates a list of text strings to a target language.

    Args:
        texts: A list of strings to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A list of translated text strings, in the same order as the input.
    """
    if not texts:
        return []

    client = get_translation_client()
    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )
    return [result["translatedText"] for result in results]
