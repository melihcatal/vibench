import os
from google.cloud import translate_v2 as translate

def translate_query(text: str, target_language_code: str = 'en') -> str:
    """
    Translates a query into a target language using Google Cloud Translation.
    This is useful for multilingual semantic search where queries might be
    in different languages than the documents.
    """
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods if set up.
    # No explicit API Key handling here beyond env setup.
    
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language_code)

    return result["translatedText"]

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS are set up, e.g., via a service account JSON file
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    spanish_query = "Hola, ¿cómo estás?"
    french_query = "Quel est le meilleur restaurant?"
    
    try:
        translated_to_en_spanish = translate_query(spanish_query, 'en')
        print(f"Original Spanish: \"{spanish_query}\" -> Translated English: \"{translated_to_en_spanish}\"")

        translated_to_en_french = translate_query(french_query, 'en')
        print(f"Original French: \"{french_query}\" -> Translated English: \"{translated_to_en_french}\"")

        translated_to_fr_spanish = translate_query(spanish_query, 'fr')
        print(f"Original Spanish: \"{spanish_query}\" -> Translated French: \"{translated_to_fr_spanish}\"")
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS are correctly configured for Google Cloud Translation.")
