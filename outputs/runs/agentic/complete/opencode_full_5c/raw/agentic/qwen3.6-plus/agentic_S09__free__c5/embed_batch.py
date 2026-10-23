from typing import List
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env
from embeddings_models import BatchEmbeddingRequest


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small", dimensions: int = None
) -> List[List[float]]:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    request = BatchEmbeddingRequest(
        model=model or config["default_model"] or "text-embedding-3-small",
        input_texts=texts,
        dimensions=dimensions or config["default_dimensions"],
    )
    response = client.embeddings.create(
        model=request.model,
        input=request.input_texts,
        encoding_format="float",
        dimensions=request.dimensions,
    )
    sorted_data = sorted(response.data, key=lambda x: x.index)
    embeddings = [item.embedding for item in sorted_data]
    return embeddings


if __name__ == "__main__":
    texts = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Python is a popular programming language",
    ]
    results = embed_batch(texts)
    for i, emb in enumerate(results):
        print(f"Text {i + 1} embedding dimensions: {len(emb)}")
