from typing import List
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(
    text: str, model: str = "text-embedding-3-small", dimensions: int = None
) -> List[float]:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    request = EmbeddingRequest(
        model=model or config["default_model"] or "text-embedding-3-small",
        input_text=text,
        dimensions=dimensions or config["default_dimensions"],
    )
    response: EmbeddingResponse = client.embeddings.create(
        model=request.model,
        input=request.input_text,
        encoding_format="float",
        dimensions=request.dimensions,
    )
    embedding = response.data[0].embedding
    return embedding


if __name__ == "__main__":
    result = embed_text("The quick brown fox jumps over the lazy dog")
    print(f"Embedding dimensions: {len(result)}")
    print(f"First 5 values: {result[:5]}")
