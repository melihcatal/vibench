import os
from typing import List, Dict, Any
from google import genai


def summarize_embedding_job(
    texts: List[str],
    embeddings: List[List[float]],
    model: str = "text-embedding-3-small",
) -> str:
    """Summarize embedding job results."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    client = genai.Client(api_key=api_key)

    text_count = len(texts)
    embedding_dim = len(embeddings[0]) if embeddings else 0

    prompt = f"""
    Summarize the results of an embedding job:
    - Number of texts processed: {text_count}
    - Embedding dimension: {embedding_dim}
    - Model used: {model}
    
    Provide a concise summary of what was accomplished and any notable observations.
    """

    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)

    return response.text
