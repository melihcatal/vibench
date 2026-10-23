from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    """Translates text extracted from a stored document."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']