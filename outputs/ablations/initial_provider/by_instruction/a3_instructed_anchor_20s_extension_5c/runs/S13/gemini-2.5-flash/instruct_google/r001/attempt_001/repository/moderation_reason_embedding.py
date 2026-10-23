from typing import List
from safety_client import SafetyClient
from safety_models import EmbeddingResult

def embed_moderation_reason(reason_text: str) -> EmbeddingResult:
    client = SafetyClient()
    embedding_model = client.get_embedding_model()

    # Google Cloud Vertex AI Text Embedding API is the concrete external provider.
    # The model ID 'text-embedding-004' is a specific provider-identifying signal.
    
    # The Vertex AI SDK returns an Embedding object directly for text inputs.
    embeddings = embedding_model.get_embeddings([reason_text])
    
    # The embedding is a list of floats
    embedding_vector = embeddings[0].values

    return EmbeddingResult(
        text=reason_text,
        embedding=embedding_vector,
        provider="Google Cloud Vertex AI Text Embedding API (text-embedding-004)"
    )

