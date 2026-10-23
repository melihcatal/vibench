import os
import cohere
from typing import List, Union


def embed_output(texts: Union[str, List[str]]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required.")
    co = cohere.Client(api_key)
    if isinstance(texts, str):
        texts = [texts]
    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
