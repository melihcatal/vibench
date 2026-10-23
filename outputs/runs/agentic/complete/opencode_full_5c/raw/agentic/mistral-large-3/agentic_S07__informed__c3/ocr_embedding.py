import cohere
import os
from typing import List, Dict, Any


def ocr_embedding(text: str, input_type: str = "search_document") -> List[float]:
    """
    Embeds extracted document sections for semantic retrieval using Cohere Embed API.

    Args:
        text: Extracted document text or section to embed.
        input_type: Type of input (e.g., "search_document", "search_query").

    Returns:
        List of floats representing the embedding vector.
    """
    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        raise ValueError("Cohere API key not configured.")

    co = cohere.Client(api_key)

    response = co.embed(texts=[text], model="embed-english-v3.0", input_type=input_type)

    return response.embeddings[0]
