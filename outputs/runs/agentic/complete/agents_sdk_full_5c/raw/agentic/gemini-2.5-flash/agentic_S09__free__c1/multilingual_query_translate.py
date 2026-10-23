from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

def multilingual_query_translate(query: str, target_language: str, project_id: str) -> Dict[str, Any]:
    """Translates queries before multilingual embedding search using Google Cloud Translation API.

    Args:
        query: The query string to translate.
        target_language: The ISO 639-1 code of the target language (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID (for client configuration).

    Returns:
        A dictionary containing the original query, translated text, and detected source language.
    """
    translate_client = translate.Client(project=project_id)

    result = translate_client.translate(query, target_language=target_language)

    return {
        "original_query": query,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "translation_provider": "Google Cloud Translation API"
    }

if __name__ == '__main__':
    # Example usage:
    # project_id = "YOUR_PROJECT_ID"
    # english_query = "What is the weather like today?"
    # spanish_query = "¿Cómo está el clima hoy?"

    # translated_to_spanish = multilingual_query_translate(english_query, "es", project_id)
    # print(f"English to Spanish translation: {translated_to_spanish}")

    # translated_to_french = multilingual_query_translate(spanish_query, "fr", project_id)
    # print(f"Spanish to French translation: {translated_to_french}")
    pass
