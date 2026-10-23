from google.cloud import translate_v2 as translate

def translate_text(project_id: str, text: str, target_language: str = "en") -> str:
    """Translates the given text to the target language using Google Cloud Translation API."""
    translate_client = translate.Client(project=project_id)
    
    # Target can be a language code, such as "en", "es", "fr", etc.
    result = translate_client.translate(text, target_language=target_language)
    
    return result['translatedText']

