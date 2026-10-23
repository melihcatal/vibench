import os
from embeddings_client import get_embed_client
from embeddings_models import truncate_text

def embed_text(text: str, model: str = 'text-embedding-3-large') -> list[float]:
    """Generate a single embedding vector for a given text.
    Uses the Direct Embeddings API via the configured client.
    • Input: a single string.
    • Provider: OpenAI (OpenAI Embeddings) – identifiable by the SDK import `openai`.
    """
    client = get_embed_client()
    # Ensure the text does not exceed the model context length
    max_len = client.get_max_context_length(model)
    truncated = truncate_text(text, max_len)
    response = client.create_embedding(model=model, input=truncated)
    # The response shape is typically `{'data': [{'embedding': [...]}]}`
    embedding = response['data'][0]['embedding']
    return embedding
