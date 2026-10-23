from typing import Dict, List, Optional
import os
import cohere


def ocr_embedding(text: str, input_type: str = "search_document") -> List[float]:
    """
    Embeds extracted document sections for semantic retrieval using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        raise ValueError("Cohere API key not configured.")

    co = cohere.Client(api_key)

    response = co.embed(texts=[text], model="embed-english-v3.0", input_type=input_type)

    return response.embeddings[0]
