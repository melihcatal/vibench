import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv() # Load environment variables

def translate_query(text: str, target_language: str = "en") -> str:
    """
    Translates a query text into a target language using Google Cloud Translation.
    
    Args:
        text: The query text to translate.
        target_language: The ISO 639-1 code of the target language (e.g., "en", "es", "fr").
                         Defaults to "en" (English).
                         
    Returns:
        The translated text.
    """
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure this environment variable points to your service account key file.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        # For local testing, you might need to set this explicitly or use gcloud auth application-default login
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Translation might fail without proper authentication.")
    
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return text # Return original text on error

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # Set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    # spanish_query = "Hola, ¿cómo estás?"
    # french_query = "Quel est le temps qu'il fait?"
    
    # print(f"Original Spanish query: '{spanish_query}'")
    # translated_to_english = translate_query(spanish_query, "en")
    # print(f"Translated to English: '{translated_to_english}'")
    
    # print(f"\nOriginal French query: '{french_query}'")
    # translated_to_spanish = translate_query(french_query, "es")
    # print(f"Translated to Spanish: '{translated_to_spanish}'")
    pass
