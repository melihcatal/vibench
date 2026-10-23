from embeddings_client import get_google_translate_client

def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translates a query to the target language for multilingual embedding search
    using the Google Cloud Translate API.

    Args:
        query: The text to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        The translated text.
    """
    translate_client = get_google_translate_client()
    
    result = translate_client.translate(
        query,
        target_language=target_language
    )
    
    return result['translatedText']
