import numpy as np
from model_client import get_llm_client
from model_models import InferenceResponse

def embed_output(text: str, model_family: str = "text-embedding-ada-002") -> np.ndarray:
    """Generate an embedding vector for the provided text using a hosted embedding model.

    Args:
        text: The input text to embed.
        model_family: Identifier for the embedding model (default: OpenAI's ada-002 style).

    Returns:
        A numpy array representing the embedding.
    """
    client = get_llm_client(model_family)
    payload = {
        "model": model_family,
        "input": text,
        "dimensions": 1536,  # Example dimension for ada-002
    }
    response = client.embeddings(payload)  # type: ignore
    # Assume response contains a list/array of floats named 'data' or 'embedding'
    embedding = np.array(response.data)  # type: ignore
    return embedding
