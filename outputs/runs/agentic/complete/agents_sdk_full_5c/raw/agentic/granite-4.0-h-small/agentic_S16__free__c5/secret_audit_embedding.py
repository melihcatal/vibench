# [LATER-STEP] secret_audit_embedding.py
from typing import List
from security_models import SecretReference, EmbeddingContext
import random  # placeholder for real embedding model

def embed_audit_note(secret: SecretReference, note: str) -> EmbeddingContext:
    """Generate a vector embedding for an audit note attached to a secret.

    Args:
        secret (SecretReference): Reference to the secret.
        note (str): Human‑readable audit note.

    Returns:
        EmbeddingContext: Contains the embedding vector.
    """
    # Dummy embedding (random vector) for demo purposes
    embedding = [random.random() for _ in range(768)]
    return EmbeddingContext(
        secret_name=secret.name,
        notes=note,
        embedding=embedding,
    )
