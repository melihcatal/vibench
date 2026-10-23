from embeddings_client import get_gemini_embeddings_client
from embeddings_models import EMBEDDING_MODEL_NAME, normalize_embedding_values


def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Gemini Embeddings."""
    genai = get_gemini_embeddings_client()
    try:
        response = genai.embed_content(model=EMBEDDING_MODEL_NAME, content=text)
        # For single text, response.embedding is the Embedding object
        if hasattr(response, "embedding"):
            return normalize_embedding_values(response.embedding)
    except Exception as e:
        print(f"Error embedding text: {e}")
    return []
