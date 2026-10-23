from google.cloud import translate_v2 as translate

def payload_translate(text: str, target_language: str = 'es') -> str:
    """
    Translate customer-facing message payload text
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']