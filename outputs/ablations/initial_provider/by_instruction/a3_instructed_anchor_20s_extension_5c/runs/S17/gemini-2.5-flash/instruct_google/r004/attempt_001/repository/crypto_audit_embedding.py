from google.cloud import aiplatform
import os

def embed_audit_notes(project_id: str, location: str, audit_notes: list[str]) -> list[list[float]]:
    """Embeds crypto audit notes using Google Cloud Vertex AI Embeddings for semantic search.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region for Vertex AI (e.g., "us-central1").
        audit_notes: A list of audit notes (strings) to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)

    # Use the pre-trained text-embedding-004 model
    # The exact model ID might vary or evolve, but `text-embedding-004` is a common choice.
    # Check Vertex AI documentation for the latest recommended model names.
    model_name = "text-embedding-004"
    try:
        model = aiplatform.Endpoint.from_pretrained(model_name)
    except Exception as e:
        # Fallback to a different approach if from_pretrained fails, e.g., using TextEmbeddingModel.from_pretrained
        # Or more robust error handling for model not found/permissions
        print(f"Could not load model using Endpoint.from_pretrained, trying TextEmbeddingModel: {e}")
        model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)


    embeddings = []
    if audit_notes:
        # The `predict` method of TextEmbeddingModel is suitable for batch embeddings.
        # Ensure the model and API support the desired batch size.
        # For very large lists, you might need to chunk `audit_notes`.
        response = model.predict(audit_notes)
        for embedding_obj in response.embeddings:
            embeddings.append(embedding_obj.values)

    return embeddings
