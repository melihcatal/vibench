import os
from safety_client import SafetyClient
from safety_models import ModerationResult

def embed_reasons(reasons: List[str]) -> List[list[float]]:
    """Embed moderation rationales using Amazon Titan Text Embeddings.

    Uses the same AWS credentials as SafetyClient.
    Returns a list of embedding vectors (list of floats).
    """
    client = SafetyClient()
    # Titan embeddings endpoint (via Comprehend's Embedding API placeholder)
    embeddings = client.embed_content(texts=reasons)
    # embeddings format assumed: [{'embedding': [0.1, 0.2, ...]}, ...]
    return [vec['embedding'] for vec in embeddings]
