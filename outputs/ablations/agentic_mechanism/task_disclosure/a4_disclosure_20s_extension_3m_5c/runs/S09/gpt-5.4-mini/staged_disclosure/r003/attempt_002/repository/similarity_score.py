import os
from typing import List

import openai


def _embed(text: str) -> List[float]:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def cosine_similarity(text_a: str, text_b: str) -> float:
    embedding_a = _embed(text_a)
    embedding_b = _embed(text_b)
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)
