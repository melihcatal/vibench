from embeddings_client import create_client, embedding_model_name
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_embedding


def embed_text(text: str) -> EmbeddingResponse:
    request = EmbeddingRequest(text=text)
    client = create_client()
    model = embedding_model_name()
    result = client.models.embed_content(model=model, contents=request.text)
    embedding = normalize_embedding(result.embeddings[0].values)
    return EmbeddingResponse(embedding=embedding)
