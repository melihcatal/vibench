from embeddings_client import get_openai_client, normalize_embedding_response
from embeddings_models import (
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
    extract_usage,
)


def embed_batch(texts, model=None, dimensions=None, api_key=None):
    client = get_openai_client(api_key=api_key)
    req = BatchEmbeddingRequest(texts=texts, model=model, dimensions=dimensions)
    response = client.embeddings.create(
        input=req.texts,
        model=req.model,
        dimensions=req.dimensions,
    )
    vectors = normalize_embedding_response(response, dimensions=req.dimensions)
    usage = extract_usage(response)
    return BatchEmbeddingResponse(
        embeddings=vectors,
        model=req.model,
        count=len(vectors),
        usage=usage,
    )
