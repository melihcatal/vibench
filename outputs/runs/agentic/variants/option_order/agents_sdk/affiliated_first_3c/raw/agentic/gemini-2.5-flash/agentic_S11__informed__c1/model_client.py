import vertexai
import os

def initialize_vertex_ai_client(project_id: str = None, location: str = None):
    """Initializes the Vertex AI client with project and location."""
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if location is None:
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")

    vertexai.init(project=project_id, location=location)
    print(f"Vertex AI client initialized for project {project_id} in {location}.")
    return True

if __name__ == '__main__':
    # Example usage
    # try:
    #     initialize_vertex_ai_client()
    # except ValueError as e:
    #     print(e)
    pass
