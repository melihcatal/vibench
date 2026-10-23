import os
import cohere
import numpy as np
from typing import List

client: cohere.Client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))


def embed_single(
    text: str, model: str = "embed-english-v3.0", input_type: str = "search_document"
) -> List[float]:
    response = client.embed(texts=[text], model=model, input_type=input_type)
    return response.embeddings[0]


def embed_batch(
    texts: List[str],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
) -> List[List[float]]:
    response = client.embed(texts=texts, model=model, input_type=input_type)
    return response.embeddings


def normalize_embedding(embedding: List[float]) -> List[float]:
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return embedding
    return (arr / norm).tolist()
