from google.cloud import translate_v2 as translate
from typing import List, Dict

def translate_queries(project_id: str, queries: List[str], target_language: str = "en") -> Dict[str, str]:
    """Translates a list of queries to a target language using Google Cloud Translation API.

    Args:
        project_id: Your Google Cloud project ID.
        queries: A list of query strings to translate.
        target_language: The ISO-639-1 code of the target language (default: "en").

    Returns:
        A dictionary mapping original queries to their translated versions.
    """
    # Instantiates a client
    translate_client = translate.Client(project=project_id)

    translations = {}
    for query in queries:
        result = translate_client.translate(query, target_language=target_language)
        translations[query] = result["translatedText"]

    return translations

if __name__ == '__main__':
    # Example usage:
    # # Replace with your actual project_id
    # PROJECT_ID = "your-project-id"

    # sample_queries = [
    #     "¿Qué es el aprendizaje automático?",
    #     "Comment va le monde?"
    # ]

    # translated_queries_map = translate_queries(
    #     project_id=PROJECT_ID,
    #     queries=sample_queries,
    #     target_language="en"
    # )
    # for original, translated in translated_queries_map.items():
    #     print(f"Original: \"{original}\" -> Translated: \"{translated}\"")
    pass
