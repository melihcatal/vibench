import os
from typing import List
import cohere


def ocr_embedding(text: str) -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not set")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings[0]
