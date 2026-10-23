import embeddings_client
import embeddings_models
from typing import List

def embed_text(text: str) -> List[float]:
    """Generates an embedding vector for a single text string using OpenAI Embeddings.

    Args:
        text: The input text string.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai = embeddings_client.get_openai_client()
    model_name = embeddings_client.get_embedding_model_name()

    prepared_text = embeddings_models.prepare_text_for_embedding(text)

    response = openai.Embedding.create(
        input=[prepared_text],
        model=model_name
    )

    embeddings = embeddings_models.normalize_embedding_response(response)
    if embeddings:
        return embeddings[0]
    return []

