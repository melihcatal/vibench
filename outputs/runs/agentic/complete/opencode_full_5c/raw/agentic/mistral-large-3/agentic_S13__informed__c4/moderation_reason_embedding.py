from typing import List, Dict
from cohere import Client
import os


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    """Embed moderation rationales for case retrieval using Cohere Embed API."""
    client = Client(api_key=os.getenv("COHERE_API_KEY"))

    response = client.embed(
        texts=rationales, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
