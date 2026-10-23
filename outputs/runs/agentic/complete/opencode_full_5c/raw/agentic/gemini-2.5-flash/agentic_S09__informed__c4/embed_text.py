import os
from embeddings_client import get_gemini_client, get_embedding_model_name
from embeddings_models import normalize_embedding_response
from typing import List


def embed_text(text: str) -> List[float]:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings."""
    genai = get_gemini_client()
    model_name = get_embedding_model_name()

    response = genai.embed_content(
        model=model_name, content=text, task_type="RETRIEVAL_DOCUMENT"
    )

    # The normalize_embedding_response returns List[List[float]], so we take the first one
    return normalize_embedding_response(response)[0]
