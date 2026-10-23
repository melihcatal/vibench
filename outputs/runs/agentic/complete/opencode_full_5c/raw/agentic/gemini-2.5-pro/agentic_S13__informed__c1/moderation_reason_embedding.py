import os
from typing import List
import cohere


def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Embeds a list of moderation reason texts using the Cohere API.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    co = cohere.Client(api_key)

    response = co.embed(
        texts=reasons, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
