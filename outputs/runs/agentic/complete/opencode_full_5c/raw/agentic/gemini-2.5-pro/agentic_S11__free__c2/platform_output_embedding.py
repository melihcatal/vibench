import os
import cohere
from typing import List


def embed_text(texts: List[str]) -> List[List[float]]:
    """
    Embeds platform outputs using Cohere's embedding API.
    """
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))

    response = client.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
