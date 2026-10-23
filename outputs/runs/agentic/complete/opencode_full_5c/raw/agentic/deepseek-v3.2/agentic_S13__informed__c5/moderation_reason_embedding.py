import os
from typing import List
import cohere


def moderation_reason_embedding(reason_text: str) -> List[float]:
    """
    Embed moderation rationales for case retrieval using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=[reason_text], model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings[0]
