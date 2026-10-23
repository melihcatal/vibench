import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

client = translate.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    """Translate queries for multilingual embedding search using Google Cloud Translation."""
    results = client.translate(queries, target_language=target_language)
    return [result["translatedText"] for result in results]
