import os
from translation_client import TranslationClient
from translation_models import EmbeddingRequest
from typing import List

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_translation_memory_embeddings(request: EmbeddingRequest) -> List[List[float]]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    embeddings = client.get_text_embeddings(request.text_segments)
    return embeddings
