import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import initialize_vertex_ai, get_model_id
import os


def select_platform_resource(preferred_model_name: str) -> str:
    """Resolves a provider-specific model, deployment, or inference resource before invocation.

    Args:
        preferred_model_name: The desired model name (e.g., "gemini-pro").

    Returns:
        The resolved model ID.
    """
    project_id, location = initialize_vertex_ai()

    # In Vertex AI, selecting a model resource is primarily about specifying its ID.
    # We can perform a basic check if the model is generally available.
    # For more advanced scenarios, one might list models or check specific deployments.
    resolved_model_id = get_model_id(preferred_model_name)

    # A simple way to 'resolve' without actually listing all models for simplicity
    # In a real scenario, you might call client.list_models() and filter.
    print(
        f"Selected Vertex AI model resource: {resolved_model_id} in project {project_id}, location {location}"
    )

    return resolved_model_id
