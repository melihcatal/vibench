from typing import List, Optional
import openai

OPENAI_API_KEY = ""
EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client(api_key: Optional[str] = None) -> openai.OpenAI:
    key = api_key or OPENAI_API_KEY
    return openai.OpenAI(api_key=key)


def embed_script(
    text: str,
    model: str = EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[float]:
    client = get_openai_client(api_key)
    kwargs = {"input": text, "model": model}
    if dimensions:
        kwargs["dimensions"] = dimensions
    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def embed_scripts_batch(
    texts: List[str],
    model: str = EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    client = get_openai_client(api_key)
    kwargs = {"input": texts, "model": model}
    if dimensions:
        kwargs["dimensions"] = dimensions
    response = client.embeddings.create(**kwargs)
    embeddings = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in embeddings]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
