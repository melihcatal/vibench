from google.cloud import translate_v2 as translate

def translate_text_from_document(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates text extracted from a stored document using Google Cloud Translation.

    Args:
        text: The text content to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English). Defaults to "en".

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    return result["translatedText"]
