import os
from google.cloud import translate_v2 as translate

def translate_query(query: str, target_language: str = 'en') -> str:
    """
    Translates a query into a target language using Google Cloud Translation.
    
    Args:
        query: The query string to translate.
        target_language: The ISO 639-1 code of the target language (e.g., 'en', 'es', 'fr').
    
    Returns:
        The translated query string.
    """
    # Google Cloud Translation client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if set.
    # No explicit API key is set directly in the client constructor for this client.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key file
    # or that ADC is configured in the environment.
    
    translate_client = translate.Client()

    result = translate_client.translate(
        query,
        target_language=target_language
    )
    return result['translatedText']

if __name__ == '__main__':
    # Example usage (requires Google Cloud authentication, e.g., GOOGLE_APPLICATION_CREDENTIALS)
    
    original_query_es = "Hola mundo"
    original_query_fr = "Comment ça va?"

    try:
        translated_query_es_to_en = translate_query(original_query_es, target_language='en')
        print(f"Original (Spanish): '{original_query_es}' -> Translated (English): '{translated_query_es_to_en}'")

        translated_query_fr_to_en = translate_query(original_query_fr, target_language='en')
        print(f"Original (French): '{original_query_fr}' -> Translated (English): '{translated_query_fr_to_en}'")
        
        # Translate an English query to Spanish
        english_query = "What is the weather like today?"
        translated_query_en_to_es = translate_query(english_query, target_language='es')
        print(f"Original (English): '{english_query}' -> Translated (Spanish): '{translated_query_en_to_es}'")

    except Exception as e:
        print(f"Error during translation: {e}")
        print("Please ensure Google Cloud authentication is properly configured (e.g., GOOGLE_APPLICATION_CREDENTIALS).")
