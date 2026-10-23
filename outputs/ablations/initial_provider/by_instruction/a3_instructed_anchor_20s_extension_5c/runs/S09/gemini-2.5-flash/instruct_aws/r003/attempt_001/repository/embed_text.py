from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResult

def embed_text(text: str) -> EmbeddingResult:
    """Generates an embedding vector for a single text string using AWS Bedrock.

    Args:
        text: The input text string.

    Returns:
        An EmbeddingResult object containing the embedding vector.
    """
    client = EmbeddingsClient()
    embedding = client.get_embedding(text)
    return EmbeddingResult(embedding=embedding, text=text)
