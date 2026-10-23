# [LATER-STEP] platform_output_embedding.py
# Embed platform outputs for evaluation or retrieval

from ibm_watsonx_ai import NaturalLanguageEmbedding
from model_models import ProviderResponse


def embed_output(text: str, model_id: str = "text-embedding-ada-002") -> List[float]:
    """Generate an embedding vector for the provided text using watsonx.ai embeddings."""
    client = NaturalLanguageEmbedding()
    embedding = client.encode(text, model_id=model_id)
    # The SDK returns a list of floats representing the vector
    return embedding
