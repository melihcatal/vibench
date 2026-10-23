from embeddings_client import get_gemini_embeddings_client
from embeddings_models import parse_batch_embedding_response
from typing import List


def embed_batch(
    texts: List[str], model_name: str = "models/embedding-001"
) -> List[List[float]]:
    """Generates embeddings for a batch of text strings using Google Gemini Embeddings.

    Args:
        texts: A list of text strings to embed.
        model_name: The name of the embedding model to use.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector for a corresponding text.
    """
    genai = get_gemini_embeddings_client()
    # The genai.embed_content function directly handles a list of texts for batch embedding
    response = genai.embed_content(model=model_name, content=texts)
    embeddings = parse_batch_embedding_response(response)
    return embeddings
