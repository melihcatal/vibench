import os
from openai import OpenAI


def embed_script(text: str, model: str = "text-embedding-3-small") -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding


def embed_scripts_batch(
    texts: list[str], model: str = "text-embedding-3-small"
) -> list[list[float]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=texts,
        model=model,
    )
    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in sorted_data]


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search_voice_assets(
    query: str,
    asset_texts: list[str],
    asset_ids: list[str],
    model: str = "text-embedding-3-small",
    top_k: int = 5,
) -> list[dict]:
    query_embedding = embed_script(query, model=model)
    asset_embeddings = embed_scripts_batch(asset_texts, model=model)

    scored = []
    for i, embedding in enumerate(asset_embeddings):
        score = cosine_similarity(query_embedding, embedding)
        scored.append(
            {"asset_id": asset_ids[i], "score": score, "text": asset_texts[i]}
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
