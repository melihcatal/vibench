from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """
    Translates a single text string between languages using Google Cloud Translation.

    Args:
        text: The text string to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English).
                         If None, the source language will be auto-detected.

    Returns:
        The translated text string.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    translation = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        model="nmt",  # Neural Machine Translation model
    )

    return translation["translatedText"]
