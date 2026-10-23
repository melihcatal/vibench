import math
import os
from typing import Sequence

import openai


def cosine_similarity(text_a: str, text_b: str, model: str = "text-embedding-3-small") -> float:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    embeddings = client.embeddings.create(model=model, input=[text_a, text_b])
    vec_a = embeddings.data[0].embedding
    vec_b = embeddings.data[1].embedding
    return _cosine(vec_a, vec_b)


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)
