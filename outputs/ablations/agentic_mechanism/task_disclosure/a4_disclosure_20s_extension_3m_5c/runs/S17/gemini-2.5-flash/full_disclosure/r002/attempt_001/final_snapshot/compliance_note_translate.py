from google.cloud import translate_v2 as translate

def translate_compliance_note(text: str, target_language: str = "en") -> str:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
