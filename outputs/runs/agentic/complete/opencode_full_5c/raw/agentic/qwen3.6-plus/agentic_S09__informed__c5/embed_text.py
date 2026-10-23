from embeddings_client import get_openai_client, normalize_embedding_response
from embeddings_models import EmbeddingRequest, EmbeddingResponse, extract_usage


def embed_text(text, model=None, dimensions=None, api_key=None):
    client = get_openai_client(api_key=api_key)
    req = EmbeddingRequest(text=text, model=model, dimensions=dimensions)
    response = client.embeddings.create(
        input=req.text,
        model=req.model,
        dimensions=req.dimensions,
    )
    vectors = normalize_embedding_response(response, dimensions=req.dimensions)
    usage = extract_usage(response)
    return EmbeddingResponse(
        embedding=vectors[0],
        model=req.model,
        index=0,
        usage=usage,
    )
