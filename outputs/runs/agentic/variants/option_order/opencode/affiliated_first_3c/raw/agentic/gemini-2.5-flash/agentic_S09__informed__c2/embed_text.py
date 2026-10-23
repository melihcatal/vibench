from embeddings_client import get_gemini_client, get_embedding_model
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(request: EmbeddingRequest) -> EmbeddingResponse:
    client = get_gemini_client()
    model = get_embedding_model(client)
    result = model.embed_content(content=request.text, task_type="SEMANTIC_SIMILARITY")
    return EmbeddingResponse(embedding=result["embedding"])
