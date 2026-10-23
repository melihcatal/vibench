import os
from google.cloud import translate_v2 as translate

def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translates a query to a target language using Google Cloud Translation.
    
    Args:
        query: The query string to translate.
        target_language: The ISO 639-1 code of the target language (e.g., "en", "es", "fr").
        
    Returns:
        The translated query string.
    """
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure this environment variable is set or authentication is configured.
    
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            query,
            target_language=target_language
        )
        return result['translatedText']
    except Exception as e:
        print(f"Error translating query with Google Cloud Translation: {e}")
        return query # Return original query on error

