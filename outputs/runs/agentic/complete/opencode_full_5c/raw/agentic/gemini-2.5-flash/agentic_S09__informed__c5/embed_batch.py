from embeddings_client import get_gemini_embeddings_client
from embeddings_models import EMBEDDING_MODEL_NAME, normalize_embedding_values


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of texts using Gemini Embeddings."""
    genai = get_gemini_embeddings_client()
    embeddings_list = []
    try:
        response = genai.embed_content(model=EMBEDDING_MODEL_NAME, content=texts)
        if hasattr(response, "embeddings"):
            for embedding_obj in response.embeddings:
                embeddings_list.append(normalize_embedding_values(embedding_obj))
    except Exception as e:
        print(f"Error embedding batch: {e}")
    return embeddings_list
