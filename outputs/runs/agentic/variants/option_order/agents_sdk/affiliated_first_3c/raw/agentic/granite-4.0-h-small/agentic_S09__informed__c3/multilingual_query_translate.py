from google.cloud.translate_v2 import Client as TranslationClient

def multilingual_query_translate(query: str, target_lang: str = 'en') -> str:
    """Translate a query string into the target language using Google Cloud Translation."""
    client = TranslationClient()
    result = client.translate(query, target_language=target_lang)
    return result['translatedText']