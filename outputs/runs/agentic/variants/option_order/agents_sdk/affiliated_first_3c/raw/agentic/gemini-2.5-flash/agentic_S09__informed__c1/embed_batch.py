import embeddings_client
import embeddings_models
from typing import List

def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generates embedding vectors for a batch of text strings using OpenAI Embeddings.

    Args:
        texts: A list of input text strings.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector.
    """
    openai = embeddings_client.get_openai_client()
    model_name = embeddings_client.get_embedding_model_name()

    prepared_texts = embeddings_models.prepare_batch_for_embedding(texts)

    if not prepared_texts:
        return []

    response = openai.Embedding.create(
        input=prepared_texts,
        model=model_name
    )

    return embeddings_models.normalize_embedding_response(response)
