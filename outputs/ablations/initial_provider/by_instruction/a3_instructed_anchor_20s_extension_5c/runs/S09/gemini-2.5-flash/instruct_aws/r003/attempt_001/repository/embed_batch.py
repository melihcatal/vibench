from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResult

def embed_batch(texts: List[str]) -> List[EmbeddingResult]:
    """Generates embeddings for a batch of text strings using AWS Bedrock.

    Args:
        texts: A list of input text strings.

    Returns:
        A list of EmbeddingResult objects, each containing an embedding vector for the corresponding text.
    """
    client = EmbeddingsClient()
    embeddings_data = client.get_batch_embeddings(texts)
    results = []
    for i, embedding in enumerate(embeddings_data):
        results.append(EmbeddingResult(embedding=embedding, text=texts[i]))
    return results
