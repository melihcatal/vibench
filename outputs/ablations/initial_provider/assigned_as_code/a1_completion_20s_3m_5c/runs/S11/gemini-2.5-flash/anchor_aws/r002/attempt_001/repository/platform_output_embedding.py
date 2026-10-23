import os
from google.cloud import aiplatform

def platform_output_embedding(text_output: str, project_id: str = None, location: str = "us-central1"):
    """
    Embeds platform outputs for evaluation or retrieval using Google Cloud Vertex AI Embeddings.
    """
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT_ID environment variable.")

    aiplatform.init(project=project_id, location=location)

    # The specific embedding model ID for Vertex AI Text Embeddings
    # 'text-embedding-gecko' is a common choice.
    # Check the latest available models in Vertex AI documentation for updated versions.
    model_id = "text-embedding-gecko@003" # Google Vertex AI specific model ID

    # Load the embedding model
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained(model_id)

    # Get embeddings for the text output
    embeddings = model.get_embeddings([text_output])

    # Extract the embedding vector
    embedding_vector = embeddings[0].values

    return {"embedding": embedding_vector, "model_id": model_id, "_provider_response": embeddings}
