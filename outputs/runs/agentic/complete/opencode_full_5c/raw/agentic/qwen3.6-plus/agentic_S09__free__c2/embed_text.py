from embeddings_client import create_embeddings_client, handle_embedding_error
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text, model=None, dimensions=None, client=None, api_key=None):
    if not text or not text.strip():
        raise ValueError("Input text must be a non-empty string")

    if client is None:
        client, model = create_embeddings_client(model=model, api_key=api_key)

    if model is None:
        model = "text-embedding-3-small"

    request = EmbeddingRequest(
        texts=[text],
        model=model,
        dimensions=dimensions,
    )

    try:
        response = client.embeddings.create(**request.to_payload())
        result = EmbeddingResponse.from_openai_response(response)
        return result.get_embedding(0)
    except Exception as exc:
        handle_embedding_error(exc)
