from google.cloud import translate_v2 as translate

def translate_record_field(text: str, target_language: str = "es") -> str:
    """
    Translates a text field to a target language using Google Cloud Translate.

    Authentication is handled automatically via the GOOGLE_APPLICATION_CREDENTIALS
    environment variable.

    Provider: Google Cloud Translate
    """
    # Provider-identifying signal: google.cloud.translate_v2.Client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    
    return result["translatedText"]
