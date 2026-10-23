import os
from typing import List, Dict, Optional


def translate_text(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """Translate narration scripts using Google Cloud Translation."""
    from google.cloud import translate_v2 as translate

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        client = translate.Client.from_service_account_json(credentials_path)
    else:
        client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return result["translatedText"]


def translate_batch(
    texts: List[str], target_language: str = "en", source_language: Optional[str] = None
) -> List[str]:
    """Translate multiple narration scripts in batch using Google Cloud Translation."""
    from google.cloud import translate_v2 as translate

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        client = translate.Client.from_service_account_json(credentials_path)
    else:
        client = translate.Client()

    if source_language:
        results = client.translate(
            texts, target_language=target_language, source_language=source_language
        )
    else:
        results = client.translate(texts, target_language=target_language)

    return [result["translatedText"] for result in results]


def detect_language(text: str) -> Dict[str, str]:
    """Detect language of narration script using Google Cloud Translation."""
    from google.cloud import translate_v2 as translate

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        client = translate.Client.from_service_account_json(credentials_path)
    else:
        client = translate.Client()

    result = client.detect_language(text)

    return {"language": result["language"], "confidence": result["confidence"]}
