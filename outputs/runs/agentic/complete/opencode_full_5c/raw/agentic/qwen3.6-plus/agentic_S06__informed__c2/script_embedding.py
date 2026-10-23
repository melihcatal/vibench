import os
from openai import OpenAI
from typing import List, Optional


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"OpenAI API key not found. Set the {OPENAI_API_KEY_ENV} environment variable."
        )
    return OpenAI(api_key=api_key)


def embed_script(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[float]:
    client = get_openai_client()

    params = {
        "input": text,
        "model": model,
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    return response.data[0].embedding


def embed_script_batch(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    client = get_openai_client()

    params = {
        "input": texts,
        "model": model,
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    return [item.embedding for item in response.data]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
