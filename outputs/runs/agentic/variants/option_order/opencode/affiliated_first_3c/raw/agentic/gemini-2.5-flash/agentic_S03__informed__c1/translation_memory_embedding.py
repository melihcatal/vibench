import google.generativeai as genai
import os
from typing import List


def embed_segments(segments: List[str]) -> List[List[float]]:
    """Embeds translated segments for translation-memory search using Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The embedding model to use
    model = "models/embedding-001"

    embeddings = []
    for segment in segments:
        response = genai.embed_content(model=model, content=segment)
        embeddings.append(response["embedding"])

    return embeddings
