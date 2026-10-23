from vertexai.generative_models import GenerativeModel
from model_client import get_google_cloud_project, get_google_cloud_location
import vertexai


def select_model_resource(
    model_name: str = "gemini-1.5-pro-preview-0409",
) -> GenerativeModel:
    """
    Resolves a provider-specific model resource before invocation.

    Args:
        model_name: The name of the model to select.

    Returns:
        An instance of the GenerativeModel.
    """
    project_id = get_google_cloud_project()
    location = get_google_cloud_location()

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)

    model = GenerativeModel(model_name)
    return model


if __name__ == "__main__":
    try:
        model_resource = select_model_resource()
        print(f"Successfully selected model resource: {model_resource}")
    except (ValueError, ImportError) as e:
        print(f"Error selecting model resource: {e}")
