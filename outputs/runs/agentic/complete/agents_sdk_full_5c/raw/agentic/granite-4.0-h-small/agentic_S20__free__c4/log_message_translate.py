from google.cloud import translate_v2 as translate

def translate_log_message(message: str, target_language: str = "es") -> str:
    """
    Translate a support-visible log message into another locale using Google Cloud Translate.
    Requires GOOGLE_APPLICATION_CREDENTIALS env var and the translate API enabled.
    """
    client = translate.Client()
    result = client.translate(message, target_language=target_language)
    return result["translatedText"]