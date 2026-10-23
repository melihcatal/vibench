import vertexai

def initialize_vertex_ai_client(project_id: str, location: str):
    """Initializes the Google Cloud Vertex AI client."""
    vertexai.init(project=project_id, location=location)
    print(f"Vertex AI client initialized for project: {project_id}, location: {location}")

class ModelClientConfig:
    """Configuration class for model clients."""
    def __init__(self, project_id: str, location: str, model_name: str):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
