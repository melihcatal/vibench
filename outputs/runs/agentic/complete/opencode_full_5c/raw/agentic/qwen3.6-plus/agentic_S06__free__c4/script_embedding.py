import httpx
import math
from typing import List
from speech_client import (
    OPENAI_EMBEDDINGS_ENDPOINT,
    get_openai_headers,
    create_http_client,
    build_embedding_payload,
    validate_openai_key,
    DEFAULT_EMBEDDING_MODEL,
)
from speech_models import EmbeddingRequest, EmbeddingResponse


def embed_script(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> EmbeddingResponse:
    if not validate_openai_key():
        raise ValueError("OPENAI_API_KEY is not set or invalid")

    request = EmbeddingRequest(text=text, model=model)
    payload = request.to_openai_payload()

    with create_http_client() as client:
        response = client.post(
            OPENAI_EMBEDDINGS_ENDPOINT,
            headers=get_openai_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    embedding = data["data"][0]["embedding"]

    return EmbeddingResponse(
        embedding=embedding,
        model_used=data.get("model", model),
        dimensions=len(embedding),
    )


def embed_scripts_batch(
    texts: list,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list:
    results = []
    for text in texts:
        result = embed_script(text=text, model=model)
        results.append(result)
    return results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def search_voice_assets(
    query_text: str,
    asset_texts: list,
    top_k: int = 3,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list:
    query_embedding = embed_script(text=query_text, model=model)

    scored_assets = []
    for asset_text in asset_texts:
        asset_embedding = embed_script(text=asset_text, model=model)
        similarity = cosine_similarity(
            query_embedding.embedding, asset_embedding.embedding
        )
        scored_assets.append(
            {
                "text": asset_text,
                "similarity": similarity,
            }
        )

    scored_assets.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_assets[:top_k]
