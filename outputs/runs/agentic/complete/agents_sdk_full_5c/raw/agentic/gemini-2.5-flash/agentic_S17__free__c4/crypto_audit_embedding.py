
"""
crypto_audit_embedding.py - Embed crypto audit notes for semantic search using Google Cloud Vertex AI.
"""

import os
from google.cloud import aiplatform # Provider-identifying signal
from vertexai.language_models import TextEmbeddingModel # Specific Vertex AI model import
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse

def embed_audit_note(request: CryptoAuditEmbeddingRequest) -> CryptoAuditEmbeddingResponse:
    # Initialize Vertex AI SDK. Project ID and region are typically set via environment variables
    # or explicit `aiplatform.init()`. For demonstration, assume environment variables are set.
    # aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_REGION", "us-central1"))
    
    # The Vertex AI API endpoint for us-central1 is us-central1-aiplatform.googleapis.com
    # The model ID is textembedding-gecko@003 or a newer version.
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003") # Concrete model identifier
    
    # Embed the audit note
    embeddings = model.get_embeddings([request.audit_note])
    
    # The embedding result is a list of Embedding objects, each containing a list of floats.
    # We expect one embedding for one input.
    if embeddings and embeddings[0].values:
        return CryptoAuditEmbeddingResponse(embedding=embeddings[0].values)
    else:
        return CryptoAuditEmbeddingResponse(embedding=[])
