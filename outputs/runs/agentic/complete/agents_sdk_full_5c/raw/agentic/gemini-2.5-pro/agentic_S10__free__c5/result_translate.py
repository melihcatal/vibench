from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """
    Translates text into the target language using Google Cloud Translate API.
    
    Requires Google Cloud authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS).
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    
    return result['translatedText']
