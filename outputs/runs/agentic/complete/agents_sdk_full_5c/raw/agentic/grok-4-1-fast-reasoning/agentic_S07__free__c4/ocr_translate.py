from document_client import get_translate_client

def ocr_translate(text: str, target_language: str = 'es') -> str:
    client = get_translate_client()
    if not text.strip():
        return ''
    result = client.translate(text, target_language=target_language)
    return result['translatedText']