import os
from google.cloud import translate_v2 as translate
from typing import List


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """
    Translates queries to a target language using Google Cloud Translation.
    Before running, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    to the path of your service account key file, or configure authentication otherwise.
    """
    translate_client = translate.Client()

    translations = []
    for query in queries:
        result = translate_client.translate(query, target_language=target_language)
        translations.append(result["translatedText"])
    return translations


if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    sample_queries = [
        "Bonjour le monde",  # French
        "Hola, ¿cómo estás?",  # Spanish
        "Wie geht es dir?",  # German
    ]
    target_lang = "en"

    print(f"Original Queries: {sample_queries}")
    translated_queries = translate_queries(sample_queries, target_language=target_lang)
    print(f"Translated Queries ({target_lang}): {translated_queries}")

    # Example: Translate English to Spanish
    english_queries = ["Hello, how are you?", "Thank you very much."]
    spanish_translations = translate_queries(english_queries, target_language="es")
    print(f"English Queries: {english_queries}")
    print(f"Translated Queries (es): {spanish_translations}")
