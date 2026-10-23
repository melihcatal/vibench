from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """Translates extracted OCR text using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']
