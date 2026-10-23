import os
import google.generativeai as genai  # Provider-specific import
from typing import List


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using Gemini Embeddings.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # Specific model ID for embeddings
    embedding_model = "models/embedding-001"

    embeddings = []
    for segment in segments:
        response = genai.embed_content(
            model=embedding_model,
            content=segment,
            task_type="RETRIEVAL_DOCUMENT",  # or other relevant task type
        )
        embeddings.append(response["embedding"])
    return embeddings
