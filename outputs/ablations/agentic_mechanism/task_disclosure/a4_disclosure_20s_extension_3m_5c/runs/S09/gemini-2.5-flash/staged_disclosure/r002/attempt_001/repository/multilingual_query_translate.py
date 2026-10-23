from google.cloud import translate_v2 as translate

def translate_query(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., "en", "es", "fr").

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    query = "Hola, ¿cómo estás?"
    translated_query = translate_query(query, target_language="en")
    print(f"Original query: {query}")
    print(f"Translated query (en): {translated_query}")

    query_french = "Hello, how are you?"
    translated_query_french = translate_query(query_french, target_language="fr")
    print(f"Original query: {query_french}")
    print(f"Translated query (fr): {translated_query_french}")
