import os
import cohere
from typing import List

def embed_script(text_or_texts: str | List[str]) -> List[List[float]]:
    cohere_api_key = os.environ.get("COHERE_API_KEY")

    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    client = cohere.Client(cohere_api_key)

    if isinstance(text_or_texts, str):
        texts = [text_or_texts]
    else:
        texts = text_or_texts

    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_query" # or "classification", "clustering", "reranker", "other"
    )

    return response.embeddings
