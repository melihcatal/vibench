import os
import cohere
from typing import List


def platform_output_embedding(text: str) -> List[float]:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=[text], model="embed-english-v3.0")
    return response.embeddings[0]
