import os
import vertexai


def select_platform_resource(
    project_id: str = None,
    location: str = "us-central1",
    model_family: str = "text-bison",
) -> str:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    vertexai.init(project=project_id, location=location)

    # In a real scenario, you'd have more sophisticated logic to select a specific model
    # For this example, we'll just return a known model name from the specified family
    if model_family == "text-bison":
        return "text-bison@002"  # A specific Vertex AI model identifier
    elif model_family == "chat-bison":
        return "chat-bison@002"
    else:
        raise ValueError(f"Unknown model family: {model_family}")
