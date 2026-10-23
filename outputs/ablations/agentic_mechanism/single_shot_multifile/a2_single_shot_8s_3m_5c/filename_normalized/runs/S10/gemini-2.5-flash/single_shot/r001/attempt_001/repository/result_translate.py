from model_client import get_google_translate_client

def translate_text(text: str, target_language: str = "en", source_language: str = None) -> str:
    client = get_google_translate_client()
    
    if source_language:
        result = client.translate(text, target_language=target_language, source_language=source_language)
    else:
        result = client.translate(text, target_language=target_language)
    
    return result['translatedText']