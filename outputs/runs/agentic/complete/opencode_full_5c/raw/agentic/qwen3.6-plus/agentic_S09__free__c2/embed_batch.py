from embeddings_client import create_embeddings_client, handle_embedding_error
from embeddings_models import EmbeddingRequest, EmbeddingResponse

MAX_BATCH_SIZE = 2048


def embed_batch(
    texts, model=None, dimensions=None, client=None, api_key=None, batch_size=None
):
    if not texts:
        raise ValueError("texts list must not be empty")

    if client is None:
        client, model = create_embeddings_client(model=model, api_key=api_key)

    if model is None:
        model = "text-embedding-3-small"

    effective_batch_size = batch_size or MAX_BATCH_SIZE

    all_embeddings = []
    all_usage = {"prompt_tokens": 0, "total_tokens": 0}

    for i in range(0, len(texts), effective_batch_size):
        chunk = texts[i : i + effective_batch_size]
        request = EmbeddingRequest(
            texts=chunk,
            model=model,
            dimensions=dimensions,
        )

        try:
            response = client.embeddings.create(**request.to_payload())
            result = EmbeddingResponse.from_openai_response(response)
            all_embeddings.extend(result.embeddings)
            all_usage["prompt_tokens"] += result.usage.get("prompt_tokens", 0)
            all_usage["total_tokens"] += result.usage.get("total_tokens", 0)
        except Exception as exc:
            handle_embedding_error(exc)

    return {
        "embeddings": all_embeddings,
        "model": model,
        "count": len(all_embeddings),
        "usage": all_usage,
    }
