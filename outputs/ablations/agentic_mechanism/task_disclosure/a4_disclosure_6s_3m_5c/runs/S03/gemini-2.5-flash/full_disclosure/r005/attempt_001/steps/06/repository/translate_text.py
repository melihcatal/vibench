from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """Translates a single text string between languages using Google Cloud Translation API.

    Args:
        text: The text string to translate.
        target_language: The target language code (e.g., "en", "es").
        source_language: The source language code (e.g., "en", "es"). If not provided,
                         the API will attempt to auto-detect the source language.

    Returns:
        The translated text string.
    """
    client = translate.Client()

    if source_language:
        result = client.translate(text, target_language=target_language, source_language=source_language)
    else:
        result = client.translate(text, target_language=target_language)

    return result["translatedText"]
