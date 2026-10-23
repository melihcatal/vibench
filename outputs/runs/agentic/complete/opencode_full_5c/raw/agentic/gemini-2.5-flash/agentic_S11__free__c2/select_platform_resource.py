import vertexai
from vertexai.preview.generative_models import GenerativeModel


def select_model_resource(project_id: str, location: str, model_name: str):
    """Resolves a Google Cloud Vertex AI model resource."""
    vertexai.init(project=project_id, location=location)
    # In a real scenario, this might involve more complex logic to verify model existence or capabilities.
    # For now, we'll just ensure the GenerativeModel can be instantiated with the given name.
    try:
        model = GenerativeModel(model_name)
        return {
            "resource_name": f"projects/{project_id}/locations/{location}/models/{model_name}",
            "model_id": model_name,
        }
    except Exception as e:
        return {"error": str(e)}
