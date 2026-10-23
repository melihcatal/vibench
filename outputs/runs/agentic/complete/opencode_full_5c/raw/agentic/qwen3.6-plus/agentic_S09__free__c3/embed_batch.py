from embeddings_client import (
    get_openai_client,
    build_batch_embedding_payload,
    extract_all_embeddings,
    extract_usage,
)
from embeddings_models import (
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
    OPENAI_EMBEDDING_MODEL,
)


def embed_batch(texts, model=OPENAI_EMBEDDING_MODEL, dimensions=1536, api_key=None):
    client = get_openai_client(api_key=api_key)
    request = BatchEmbeddingRequest(
        model=model, input_texts=texts, dimensions=dimensions
    )
    payload = build_batch_embedding_payload(
        model=request.model,
        input_texts=request.input_texts,
        dimensions=request.dimensions,
    )
    response = client.embeddings.create(**payload)
    embeddings = extract_all_embeddings(response)
    usage = extract_usage(response)
    return BatchEmbeddingResponse(
        embeddings=embeddings,
        model=model,
        usage=usage,
    )


if __name__ == "__main__":
    import sys

    texts = sys.argv[1:] if len(sys.argv) > 1 else ["Hello world", "Goodbye world"]
    result = embed_batch(texts)
    print(f"Batch size: {len(result)}")
    print(f"Model: {result.model}")
    print(f"Usage: {result.usage}")
    for i, emb in enumerate(result.embeddings):
        print(f"  [{i}] dim={len(emb)}, first_3={emb[:3]}")
