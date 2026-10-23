from google.cloud import language_v1
from translation_client import get_translation_client

_PROVIDER = "google"


def quality_summary(text: str) -> dict:
    client = get_translation_client()
    return client.summarize_quality(text)
