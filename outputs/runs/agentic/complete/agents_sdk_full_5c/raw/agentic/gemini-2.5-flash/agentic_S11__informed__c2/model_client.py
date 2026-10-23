import vertexai
import os

def initialize_vertex_ai(project_id: str = None, location: str = None):
    """
    Initializes the Vertex AI SDK.
    
    Args:
        project_id: Your Google Cloud project ID. If None, it tries to get from env var or gcloud config.
        location: The region for Vertex AI. If None, it tries to get from env var or default.
    """
    if not project_id:
        project_id = os.environ.get("GCP_PROJECT_ID")
    if not location:
        location = os.environ.get("GCP_LOCATION", "us-central1")
        
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    vertexai.init(project=project_id, location=location)
    # print(f"Vertex AI initialized for project {project_id} in location {location}")

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or you are authenticated via gcloud
    # project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    # location = os.environ.get("GCP_LOCATION", "us-central1")
    # try:
    #     initialize_vertex_ai(project_id, location)
    #     print("Vertex AI client initialized successfully.")
    # except Exception as e:
    #     print(f"Failed to initialize Vertex AI client: {e}")
