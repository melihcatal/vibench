from google.cloud import translate_v2 as translate

def ocr_translate(text: str, target_language: str = 'es') -> str:
    """
    Translate extracted OCR text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']
