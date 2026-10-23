import os
from typing import Optional
from google.cloud import translate_v2 as translate


def translate_query(query: str, target_language: str = "en") -> Optional[str]:
    api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_API_KEY environment variable not set")

    client = translate.Client()
    try:
        result = client.translate(query, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Google Translate API error: {e}")