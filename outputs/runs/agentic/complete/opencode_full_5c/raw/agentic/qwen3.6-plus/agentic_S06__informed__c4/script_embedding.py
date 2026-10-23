import os
from openai import OpenAI


def embed_script(text: str, model: str = "text-embedding-3-small") -> list:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding


def embed_scripts_batch(texts: list, model: str = "text-embedding-3-small") -> list:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=texts,
        model=model,
    )
    return [item.embedding for item in response.data]


def cosine_similarity(vec_a: list, vec_b: list) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def search_voice_assets(
    query: str,
    asset_texts: list,
    asset_embeddings: list,
    top_k: int = 5,
    model: str = "text-embedding-3-small",
) -> list:
    query_embedding = embed_script(query, model=model)
    scores = []
    for i, asset_emb in enumerate(asset_embeddings):
        score = cosine_similarity(query_embedding, asset_emb)
        scores.append((i, asset_texts[i], score))
    scores.sort(key=lambda x: x[2], reverse=True)
    return scores[:top_k]
