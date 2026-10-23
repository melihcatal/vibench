from model_client import create_openai_client, execute_embedding
from model_models import EmbeddingRequest, EmbeddingResponse

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_HOST = "api.openai.com"


def generate_embeddings(
    texts: str | list[str],
    dimensions: int | None = None,
    api_key: str | None = None,
) -> EmbeddingResponse:
    client = create_openai_client(api_key=api_key)
    request = EmbeddingRequest(
        model=OPENAI_EMBEDDING_MODEL,
        input=texts,
        dimensions=dimensions,
    )
    return execute_embedding(client, request)


def embed_single(
    text: str, dimensions: int | None = None, api_key: str | None = None
) -> list[float]:
    response = generate_embeddings(text, dimensions=dimensions, api_key=api_key)
    return response.embeddings[0]


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
