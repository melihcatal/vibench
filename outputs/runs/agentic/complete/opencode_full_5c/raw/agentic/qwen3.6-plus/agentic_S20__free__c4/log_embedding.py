import os
from openai import OpenAI
from observability_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_DIMENSIONS = 1536


def embed_log_message(text: str, dimensions: int | None = None) -> EmbeddingResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)
    dims = dimensions or DEFAULT_DIMENSIONS

    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
        dimensions=dims,
    )

    embedding_data = response.data[0]
    vector = embedding_data.embedding

    return EmbeddingResult(
        text=text,
        embedding=vector,
        model_used=OPENAI_EMBEDDING_MODEL,
        dimensions=len(vector),
    )


def embed_log_messages(
    messages: list[str],
    dimensions: int | None = None,
) -> list[EmbeddingResult]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)
    dims = dimensions or DEFAULT_DIMENSIONS

    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=messages,
        dimensions=dims,
    )

    results = []
    for text, emb_data in zip(messages, response.data):
        vector = emb_data.embedding
        results.append(
            EmbeddingResult(
                text=text,
                embedding=vector,
                model_used=OPENAI_EMBEDDING_MODEL,
                dimensions=len(vector),
            )
        )

    return results


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    sample = "TimeoutError: upstream service did not respond within 30000ms"
    result = embed_log_message(sample)
    print(f"Model: {result.model_used}")
    print(f"Dimensions: {result.dimensions}")
    print(f"Embedding preview: {result.embedding[:5]}...")
