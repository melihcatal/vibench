import os
from model_client import get_vertex_ai_embedding_model
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_text(request: EmbeddingRequest) -> EmbeddingResponse:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model = get_vertex_ai_embedding_model(project_id, location, request.model_id)

    # The TextEmbeddingModel expects a list of text instances
    embeddings = model.predict(request.texts)

    # Extract the embeddings. Each embedding is a list of floats.
    # The response object from model.predict directly contains the embeddings attribute.
    embedding_vectors = [e.values for e in embeddings.embeddings]

    return EmbeddingResponse(embeddings=embedding_vectors, model_id=request.model_id)
