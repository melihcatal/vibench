import os
from google.cloud import aiplatform
from safety_models import EmbeddingRequest, EmbeddingResponse

def embed_moderation_rationales(request: EmbeddingRequest, project_id: str, location: str = "us-central1") -> EmbeddingResponse:
    """
    Embeds moderation rationales for case retrieval using Google Cloud Vertex AI Embeddings.
    """
    # Initialize Vertex AI SDK
    aiplatform.init(project=project_id, location=location)

    # Use the pre-trained text-embedding-004 model
    # Note: The model name might vary, always check the latest available models in Vertex AI documentation.
    # For text-embedding-004, the task_type and output_dimensionality are important parameters.
    # For this task, we assume a default task_type and let the model determine output_dimensionality.
    model_id = "text-embedding-004"
    try:
        # Ensure the environment has authenticated access to Vertex AI
        # For example, by setting GOOGLE_APPLICATION_CREDENTIALS or running in a Vertex AI environment
        embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)
    except Exception as e:
        raise RuntimeError(f"Failed to load Vertex AI Embedding Model {model_id}: {e}")

    # Vertex AI embedding API can take a list of texts
    # task_type and output_dimensionality are important for specific use cases
    # For a general embedding, we can omit them, or use a general task_type like 'SEMANTIC_SIMILARITY'
    # For moderation reasons, 'SEMANTIC_SIMILARITY' or 'CLASSIFICATION' might be appropriate
    # Let's use SEMANTIC_SIMILARITY for general purpose reason embedding
    embeddings_response = embedding_model.get_embeddings(
        request.texts, 
        task_type="SEMANTIC_SIMILARITY"
    )

    # Extract embeddings from the response
    # Each item in predictions is an Embedding object with a 'values' attribute
    embedded_vectors = [embedding.values for embedding in embeddings_response.predictions]

    return EmbeddingResponse(embeddings=embedded_vectors)
