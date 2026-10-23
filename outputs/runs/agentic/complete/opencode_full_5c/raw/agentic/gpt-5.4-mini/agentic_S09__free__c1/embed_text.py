from embeddings_client import create_client, embedding_request_kwargs
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_vector


def embed_text(text: str):
    client = create_client()
    request = EmbeddingRequest(text=text)
    response = client.embeddings.create(
        input=[request.text], **embedding_request_kwargs()
    )
    vector = normalize_vector(response.data[0].embedding)
    return EmbeddingResponse(embedding=vector)
