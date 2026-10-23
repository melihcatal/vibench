import json
from google.cloud import translate_v2 as translate

def invoice_note_translate(text, target_lang="es"):
    """
    Translate extracted invoice notes/descriptions using Google Cloud Translation.
    Returns the translated text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result['translatedText']
