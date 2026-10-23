import os
import cohere
from typing import List


def get_embedding(text: str, model: str = "embed-english-v3.0") -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)
    response = co.embed(texts=[text], model=model, input_type="search_document")
    return response.embeddings[0]


def get_embeddings(
    texts: List[str], model: str = "embed-english-v3.0"
) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)
    response = co.embed(texts=texts, model=model, input_type="search_document")
    return response.embeddings
