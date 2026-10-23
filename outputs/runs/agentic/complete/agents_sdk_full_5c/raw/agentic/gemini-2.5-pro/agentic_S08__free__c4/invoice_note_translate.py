# invoice_note_translate.py
from document_client import get_google_translate_client

def translate_text(text: str, target_language: str = "en") -> dict:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    
    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.
        
    Returns:
        A dictionary containing the translated text and detected source language.
    """
    if not text.strip():
        return {"translatedText": "", "detectedSourceLanguage": "", "input": text}

    client = get_google_translate_client()
    
    result = client.translate(text, target_language=target_language)
    
    return result
