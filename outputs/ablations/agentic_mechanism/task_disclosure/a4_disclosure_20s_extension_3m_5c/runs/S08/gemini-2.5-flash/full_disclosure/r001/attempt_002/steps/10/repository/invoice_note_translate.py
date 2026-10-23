from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English).
                         If None, the service will attempt to detect the source language.

    Returns:
        The translated text.
    """
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
