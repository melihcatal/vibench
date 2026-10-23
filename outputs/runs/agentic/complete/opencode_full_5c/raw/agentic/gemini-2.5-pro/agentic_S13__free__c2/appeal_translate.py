from safety_client import get_google_translate_client


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translate.
    """
    client = get_google_translate_client()

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
