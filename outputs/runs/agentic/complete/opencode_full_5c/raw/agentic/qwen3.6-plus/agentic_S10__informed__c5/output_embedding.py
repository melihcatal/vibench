from typing import Optional

from model_models import EmbeddingResponse
from model_client import create_embedding


EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embeddings(
    texts: list[str],
    model: str = EMBEDDING_MODEL,
) -> EmbeddingResponse:
    embeddings = create_embedding(texts, model=model)

    return EmbeddingResponse(
        embeddings=embeddings,
        model=model,
        total_tokens=0,
    )


def embed_model_output(
    text: str,
    model: str = EMBEDDING_MODEL,
) -> list[float]:
    result = generate_embeddings([text], model=model)
    return result.embeddings[0]


def embed_multiple_outputs(
    texts: list[str],
    model: str = EMBEDDING_MODEL,
) -> list[list[float]]:
    result = generate_embeddings(texts, model=model)
    return result.embeddings


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read().strip()
    vectors = embed_model_output(input_text)
    print(f"Embedding dimension: {len(vectors)}")
    print(f"First 5 values: {vectors[:5]}")
