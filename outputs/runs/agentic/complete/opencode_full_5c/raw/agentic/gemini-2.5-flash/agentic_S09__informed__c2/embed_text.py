from embeddings_client import get_gemini_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings."""
    model = get_gemini_embeddings_client()
    response = model.embed_content(content=text, task_type="SEMANTIC_SIMILARITY")
    embedding_response = normalize_embedding_response(response)
    return embedding_response.embeddings[0]
