import google.generativeai as genai
import os
from typing import List

def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """Embeds translated segments for translation-memory search using Google Gemini Embeddings."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    if not segments:
        return []

    # The embedding model to use
    model = "models/embedding-001"

    # Gemini's embedding API can handle multiple texts in a single request
    response = genai.embed_content(
        model=model,
        content=segments,
        task_type="RETRIEVAL_DOCUMENT" # Appropriate task type for search/retrieval
    )

    return [embedding.values for embedding in response['embedding']]
