from translation_client import get_translation_client


def translate_text(text: str, target_language: str, source_language: str = "en"):
    """
    Translates a single text string using Google Cloud Translation.
    """
    client = get_translation_client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
