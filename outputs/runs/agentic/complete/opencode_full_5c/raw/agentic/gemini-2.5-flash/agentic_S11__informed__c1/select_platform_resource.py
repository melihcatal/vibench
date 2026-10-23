import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel


def select_vertex_ai_model_resource(
    project_id: str, location: str, model_id: str
) -> GenerativeModel:
    """
    Resolves a specific Vertex AI generative model resource.
    """
    vertexai.init(project=project_id, location=location)
    # In Vertex AI, the model_id directly corresponds to the resource.
    # We can try to instantiate it to check if it's a valid model.
    try:
        model = GenerativeModel(model_id)
        # A simple check to ensure the model can be used, e.g., by checking its name.
        # This doesn't strictly "resolve" like a deployment ID, but gets the model object.
        print(f"Successfully selected Vertex AI model resource: {model_id}")
        return model
    except Exception as e:
        raise ValueError(f"Could not resolve Vertex AI model resource {model_id}: {e}")


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Example: Select a specific model
    selected_model_id = "gemini-pro"
    try:
        model = select_vertex_ai_model_resource(
            project_id=project_id, location=location, model_id=selected_model_id
        )
        print(f"Selected model object: {model}")
        # You can now use the 'model' object for further operations
    except ValueError as e:
        print(f"Error: {e}")
