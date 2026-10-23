import vertexai
from vertexai.preview.generative_models import GenerativeModel

def select_model_resource(project_id: str, location: str, model_id: str) -> GenerativeModel:
    """
    Resolves a Vertex AI model resource.
    
    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region.
        model_id: The ID of the model to select (e.g., "gemini-pro").
        
    Returns:
        A GenerativeModel instance for the specified model.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    return model

if __name__ == '__main__':
    # Example usage
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro"

    # print(f"Selecting model resource for {model_id} in {project_id}...")
    # try:
    #     model_resource = select_model_resource(project_id, location, model_id)
    #     print(f"Successfully selected model resource: {model_resource.model_name}")
    # except Exception as e:
    #     print(f"Error selecting model resource: {e}")
