import os
from google.cloud import aiplatform

def get_vertex_ai_embedding_model(
    project_id: str = None,
    location: str = None,
    model_name: str = "text-embedding-gecko@001" # Concrete model identifier
):
    """
    Initializes and returns a Vertex AI text embedding model client.

    Args:
        project_id: Your Google Cloud project ID. If None, tries to get from env var.
        location: The GCP region. If None, tries to get from env var.
        model_name: The specific model ID to use (e.g., "text-embedding-gecko@001").

    Returns:
        An initialized google.cloud.aiplatform.Endpoint object.
    """
    if not project_id:
        project_id = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
    if not location:
        location = os.getenv("GCP_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.Endpoint.from_pretrained(model_name)
    return model

if __name__ == '__main__':
    # Example usage
    embedding_model = get_vertex_ai_embedding_model()
    print(f"Successfully initialized Vertex AI embedding model: {embedding_model.display_name}")
