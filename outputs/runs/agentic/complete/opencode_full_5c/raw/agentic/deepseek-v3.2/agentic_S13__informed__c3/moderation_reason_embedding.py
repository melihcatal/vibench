import os
from typing import List
import cohere


def moderation_reason_embedding(reason_text: str) -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        raise ValueError("Cohere API key not configured")

    client = cohere.Client(api_key)

    response = client.embed(
        texts=[reason_text], model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings[0]
