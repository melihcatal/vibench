import os
import math
from typing import List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _embed(client: OpenAI, text: str) -> List[float]:
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)


def cosine_similarity(text_a: str, text_b: str) -> float:
    client = OpenAI()
    vec_a = _embed(client, text_a)
    vec_b = _embed(client, text_b)
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("Usage: similarity_score.py <text_a> <text_b>")
    print(cosine_similarity(sys.argv[1], sys.argv[2]))
