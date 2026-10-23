import os
from model_client import get_llm_client
from model_models import LLMResponse
import numpy as np

def embed_text(text: str, model_name: str = "gpt-4o-mini-embedding") -> np.ndarray:
    """Generate an embedding vector for the given text using a hosted embedding model.
    Uses OpenAI's embedding endpoint (or any provider with similar API).
    Identifies provider via SDK import and model identifier.
    Returns a numpy array of floats.
    """
    client = get_llm_client(model_name)
    response = client.embeddings.create(
        model=model_name,
        input=text,
    )
    # Assume OpenAI-style response: data[0].embedding is list of floats
    embedding = response.data[0].embedding
    return np.array(embedding)
