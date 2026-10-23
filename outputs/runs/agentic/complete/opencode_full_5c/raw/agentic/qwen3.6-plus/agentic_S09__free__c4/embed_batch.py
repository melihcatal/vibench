from embeddings_client import (
    get_openai_client,
    create_embedding_payload,
    extract_embeddings,
    handle_openai_error,
    DEFAULT_EMBEDDING_MODEL,
)
from embeddings_models import EmbeddingRequest, EmbeddingResult, EmbeddingResponse


def embed_batch(
    texts: list, model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int = None
):
    client = get_openai_client()
    payload = create_embedding_payload(texts, model=model, dimensions=dimensions)
    try:
        response = client.embeddings.create(**payload)
        raw_embeddings = extract_embeddings(response)
        results = [
            EmbeddingResult(text=text, embedding=emb, index=i)
            for i, (text, emb) in enumerate(zip(texts, raw_embeddings))
        ]
        usage = {}
        if hasattr(response, "usage"):
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        return EmbeddingResponse(results=results, model=model, usage=usage)
    except Exception as exc:
        handle_openai_error(exc)
