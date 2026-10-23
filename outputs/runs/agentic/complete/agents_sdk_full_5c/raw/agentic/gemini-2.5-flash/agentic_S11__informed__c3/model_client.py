import vertexai

def initialize_vertex_client(project_id: str, location: str):
    """
    Initializes the Vertex AI client with specified project and location.
    """
    try:
        vertexai.init(project=project_id, location=location)
        print(f"Vertex AI client initialized for project '{project_id}' in location '{location}'.")
    except Exception as e:
        print(f"Error initializing Vertex AI client: {e}")
        raise

def get_generative_model(model_name: str):
    """
    Returns a Vertex AI GenerativeModel instance.
    """
    from vertexai.generative_models import GenerativeModel
    return GenerativeModel(model_name)

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    project_id = "your-gcp-project-id"
    location = "us-central1"
    
    initialize_vertex_client(project_id, location)
    model = get_generative_model("gemini-pro")
    print(f"Retrieved model instance: {model.model_name}")
