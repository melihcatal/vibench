import os
import vertexai

def initialize_vertex_ai_client(project_id: str = None, location: str = None):
    """
    Initializes the Vertex AI client with specified project and location.
    Reads from environment variables GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION if not provided.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if location is None:
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")

    print(f"Initializing Vertex AI client for project: {project_id}, location: {location}")
    vertexai.init(project=project_id, location=location)

def get_default_model_name() -> str:
    """Returns the default model name for the workflow."""
    return "gemini-pro"

if __name__ == '__main__':
    # Example usage
    try:
        initialize_vertex_ai_client()
        print("Vertex AI client initialized successfully.")
        print(f"Default model name: {get_default_model_name()}")
    except ValueError as e:
        print(f"Error initializing Vertex AI client: {e}")
