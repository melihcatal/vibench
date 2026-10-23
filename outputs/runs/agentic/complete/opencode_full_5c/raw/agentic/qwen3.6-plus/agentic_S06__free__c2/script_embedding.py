from speech_client import get_openai_client
from speech_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    normalize_embedding_request,
)

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str, model: str = None) -> EmbeddingResponse:
    client = get_openai_client()

    if model is None:
        model = OPENAI_EMBEDDING_MODEL

    req = EmbeddingRequest(text=text, model=model)
    payload = normalize_embedding_request(req)

    response = client.embeddings.create(**payload)
    embedding = response.data[0].embedding

    return EmbeddingResponse(
        embedding=embedding,
        model_used=model,
        dimensions=len(embedding),
    )


def embed_scripts_batch(texts: list, model: str = None) -> list:
    client = get_openai_client()

    if model is None:
        model = OPENAI_EMBEDDING_MODEL

    response = client.embeddings.create(
        input=texts,
        model=model,
    )

    results = []
    for item in response.data:
        results.append(
            EmbeddingResponse(
                embedding=item.embedding,
                model_used=model,
                dimensions=len(item.embedding),
            )
        )

    return results


def compute_similarity(embedding_a: list, embedding_b: list) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
