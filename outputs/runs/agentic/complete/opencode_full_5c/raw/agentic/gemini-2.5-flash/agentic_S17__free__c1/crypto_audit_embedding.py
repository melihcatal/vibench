import os
from security_client import get_embedding_model
from security_models import CryptoAuditEmbeddingRequest
from vertexai.language_models import TextEmbeddingModel


def embed_audit_note(request: CryptoAuditEmbeddingRequest) -> list[float]:
    model = get_embedding_model()

    # Google Cloud Vertex AI signal: vertexai.language_models.TextEmbeddingModel
    # Google Cloud Vertex AI signal: model.get_embeddings
    embeddings = model.get_embeddings([request.text])
    if embeddings:
        return embeddings[0].values
    return []
