import os
from embeddings_client import get_embed_client
from embeddings_models import truncate_texts

def embed_batch(texts: list[str], model: str = 'text-embedding-3-large') -> list[list[float]]:
    """Generate embeddings for a batch of texts.
    Uses the Direct Embeddings API via the configured client.
    • Input: list of strings.
    • Provider: OpenAI (OpenAI Embeddings) – identifiable by the SDK import `openai`.
    """
    client = get_embed_client()
    max_len = client.get_max_context_length(model)
    truncated = [truncate_text(t, max_len) for t in texts]
    response = client.create_embedding(model=model, input=truncated)
    # Assuming the API returns a list of embeddings in the same order
    return [emb['embedding'] for emb in response['data']]
