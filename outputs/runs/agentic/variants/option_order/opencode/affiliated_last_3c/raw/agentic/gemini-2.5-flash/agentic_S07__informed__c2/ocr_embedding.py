import os
from typing import List
import google.generativeai as genai


def embed_text(
    texts: List[str], model_name: str = "models/embedding-001"
) -> List[List[float]]:
    """Embeds a list of texts using Google Gemini Embeddings."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # The embedding model is specified by model_name
    response = genai.embed_content(
        model=model_name,
        content=texts,
    )

    # The embedding response will contain an 'embedding' field for each text.
    # Each embedding is a list of floats.
    embeddings = [item["embedding"] for item in response["embeddings"]]
    return embeddings
