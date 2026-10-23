from google.cloud import translate_v2 as translate

def translate_alt_text(text: str, target_language: str = "en") -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.

    Args:
        text: The image description to translate.
        target_language: The language to translate the text into (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
