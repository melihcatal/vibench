from security_client import get_openai_client
from security_models import EmbeddingRequest, EmbeddingResponse


def embed_audit_note(request: EmbeddingRequest) -> EmbeddingResponse:
    client = get_openai_client()
    response = client.embeddings.create(
        input=request.text, model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return EmbeddingResponse(embedding=embedding)
