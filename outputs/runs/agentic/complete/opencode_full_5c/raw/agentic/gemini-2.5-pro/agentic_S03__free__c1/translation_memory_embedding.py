import os
import cohere
from typing import List


def translation_memory_embedding(texts: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise EnvironmentError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
