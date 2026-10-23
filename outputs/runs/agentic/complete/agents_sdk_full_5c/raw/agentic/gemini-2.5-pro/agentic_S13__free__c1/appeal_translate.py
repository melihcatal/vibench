from google.cloud import translate_v2 as translate

def translate_appeal_text(text: str, target_language: str = "en") -> dict:
    """
    Translates appeal text for review using Google Cloud Translate.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result
