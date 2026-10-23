import os
from google.cloud import translate_v2 as translate

def multilingual_query_translate(text: str, target_language: str = "en") -> str:
    """Translates a query to a target language using Google Cloud Translation.

    Args:
        text: The query string to translate.
        target_language: The BCP-47 language code of the target language (e.g., "en", "es", "fr").

    Returns:
        The translated text string. Returns the original text if translation fails or credentials are not set.
    """
    # Google Cloud Translation client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    # Ensure your environment is authenticated (e.g., gcloud auth application-default login)
    # or GOOGLE_APPLICATION_CREDENTIALS points to a service account key file.
    
    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set and valid, or default auth is configured.")
        return text # Return original text on failure

if __name__ == '__main__':
    # Example usage (ensure Google Cloud authentication is configured)
    # from dotenv import load_dotenv
    # load_dotenv()

    # query_spanish = "¿Qué tiempo hace hoy?"
    # query_french = "Comment allez-vous?"

    # translated_to_english_es = multilingual_query_translate(query_spanish, "en")
    # translated_to_english_fr = multilingual_query_translate(query_french, "en")
    # translated_to_german_es = multilingual_query_translate(query_spanish, "de")

    # print(f"Spanish to English: '{query_spanish}' -> '{translated_to_english_es}'")
    # print(f"French to English: '{query_french}' -> '{translated_to_english_fr}'")
    # print(f"Spanish to German: '{query_spanish}' -> '{translated_to_german_es}'")
    pass
