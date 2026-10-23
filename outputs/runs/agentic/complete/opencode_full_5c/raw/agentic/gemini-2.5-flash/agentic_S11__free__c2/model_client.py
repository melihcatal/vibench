import vertexai


def initialize_vertex_ai(project_id: str, location: str):
    """Initializes the Google Cloud Vertex AI client."""
    vertexai.init(project=project_id, location=location)
    return True


# Example model ID for use across the workflow
DEFAULT_GENERATIVE_MODEL = "gemini-pro"
DEFAULT_EMBEDDING_MODEL = "text-embedding-004"
