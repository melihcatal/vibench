from embeddings_client import (
    get_openai_client,
    build_embedding_payload,
    extract_embedding_from_response,
)
from embeddings_models import EmbeddingRequest, OPENAI_EMBEDDING_MODEL


def embed_text(text, model=OPENAI_EMBEDDING_MODEL, dimensions=1536, api_key=None):
    client = get_openai_client(api_key=api_key)
    request = EmbeddingRequest(model=model, input_text=text, dimensions=dimensions)
    payload = build_embedding_payload(
        model=request.model,
        input_text=request.input_text,
        dimensions=request.dimensions,
    )
    response = client.embeddings.create(**payload)
    embedding = extract_embedding_from_response(response)
    return embedding


if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else "Hello world"
    vec = embed_text(text)
    print(f"Embedding dimension: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
