import os
import cohere
from typing import List


def output_embedding(text: str, model: str = "embed-english-v3.0") -> List[float]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    embedding = client.embed(texts=[text], model=model, input_type="search_query")
    return embedding.embeddings[0]
