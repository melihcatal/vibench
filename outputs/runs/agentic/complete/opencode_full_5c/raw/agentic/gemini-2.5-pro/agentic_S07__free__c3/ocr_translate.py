from document_client import get_google_translate_client


def translate_text(text: str, target_language: str) -> str:
    """
    Translates text to a target language using Google Cloud Translate API.
    """
    client = get_google_translate_client()

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
