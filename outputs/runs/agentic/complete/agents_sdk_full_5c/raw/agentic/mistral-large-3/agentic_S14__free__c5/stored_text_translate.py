from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "es") -> str:
    """
    Translate text extracted from a stored document using Google Cloud Translation API.
    
    Args:
        text: Text to translate.
        target_language: Target language code (e.g., 'es' for Spanish).
        
    Returns:
        Translated text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]