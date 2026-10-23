import os
from embeddings_client import get_gemini_client, get_embedding_model_name
from embeddings_models import normalize_embedding_response
from typing import List


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a batch of texts using Google Gemini Embeddings."""
    genai = get_gemini_client()
    model_name = get_embedding_model_name()

    response = genai.embed_content(
        model=model_name, content=texts, task_type="RETRIEVAL_DOCUMENT"
    )

    return normalize_embedding_response(response)
