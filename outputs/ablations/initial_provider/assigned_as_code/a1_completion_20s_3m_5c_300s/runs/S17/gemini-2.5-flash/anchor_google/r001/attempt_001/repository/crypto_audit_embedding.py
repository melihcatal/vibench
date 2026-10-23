import os
import vertexai
from vertexai.language_models import TextEmbeddingModel

# Initialize Vertex AI for the project and location
# This should ideally be done once at the application startup
_vertexai_initialized = False
_embedding_model = None

def _initialize_vertexai():
    global _vertexai_initialized, _embedding_model
    if not _vertexai_initialized:
        project_id = os.environ.get("GCP_PROJECT_ID")
        region = os.environ.get("GCP_REGION", "us-central1") # Default to us-central1
        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")

        vertexai.init(project=project_id, location=region)
        _embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        _vertexai_initialized = True

def embed_audit_note(audit_note_text: str):
    _initialize_vertexai()
    
    # The Vertex AI TextEmbeddingModel can take a list of texts, but for a single note,
    # we can just pass it directly in a list.
    embeddings = _embedding_model.get_embeddings([audit_note_text])

    # The get_embeddings method returns a list of Embedding objects. 
    # For a single input, it will be a list with one Embedding object.
    if embeddings and embeddings[0].values:
        return {
            "audit_note": audit_note_text,
            "embedding": embeddings[0].values,
            "embedding_model": "textembedding-gecko@001",
            "embedding_provider": "Google Cloud Vertex AI"
        }
    else:
        return {
            "audit_note": audit_note_text,
            "embedding": [],
            "embedding_model": "textembedding-gecko@001",
            "embedding_provider": "Google Cloud Vertex AI",
            "error": "Failed to generate embedding"
        }
