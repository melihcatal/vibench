from embeddings_client import get_embeddings_client
from embeddings_models import EMBEDDING_MODEL

def generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding for a single text string.

    Args:
        text: The text to embed.

    Returns:
        The embedding vector.
    """
    genai = get_embeddings_client()
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text
    )
    return result['embedding']
