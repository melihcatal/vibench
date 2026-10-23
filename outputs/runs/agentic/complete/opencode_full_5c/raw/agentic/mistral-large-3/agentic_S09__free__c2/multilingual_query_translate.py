from typing import List
from google.cloud import translate_v2 as translate


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """Translate queries to the target language using Google Cloud Translation API."""
    translate_client = translate.Client()

    results = []
    for query in queries:
        if not query.strip():
            results.append(query)
            continue

        result = translate_client.translate(query, target_language=target_language)
        results.append(result["translatedText"])

    return results
