from embeddings_client import get_gemini_embeddings_client
from embeddings_models import prepare_text_for_embedding, parse_embedding_response
from typing import List


def embed_text(text: str, model_name: str = "models/embedding-001") -> List[float]:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings.

    Args:
        text: The text string to embed.
        model_name: The name of the embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai = get_gemini_embeddings_client()
    # The genai.embed_content function directly handles the input text
    response = genai.embed_content(model=model_name, content=text)
    embedding = parse_embedding_response(response)
    return embedding
