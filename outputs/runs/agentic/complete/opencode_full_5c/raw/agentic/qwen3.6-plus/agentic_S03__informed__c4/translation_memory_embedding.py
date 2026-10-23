import os
from openai import OpenAI
from translation_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"
OPENAI_EMBEDDING_DIMENSIONS = 1536


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_translated_segments(
    segments: list[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=segments,
        dimensions=dimensions,
    )
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(
        vectors=vectors,
        model=model,
        dimensions=dimensions,
        segments=segments,
    )


def embed_single_segment(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=text,
        dimensions=dimensions,
    )
    return response.data[0].embedding


def search_translation_memory(
    query: str,
    memory_segments: list[str],
    memory_vectors: list[list[float]],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
) -> list[tuple[str, float]]:
    query_vector = embed_single_segment(query, model=model, dimensions=dimensions)
    similarities = []
    for i, mem_vector in enumerate(memory_vectors):
        dot_product = sum(a * b for a, b in zip(query_vector, mem_vector))
        query_magnitude = sum(a * a for a in query_vector) ** 0.5
        mem_magnitude = sum(a * a for a in mem_vector) ** 0.5
        if query_magnitude > 0 and mem_magnitude > 0:
            similarity = dot_product / (query_magnitude * mem_magnitude)
        else:
            similarity = 0.0
        similarities.append((memory_segments[i], similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
