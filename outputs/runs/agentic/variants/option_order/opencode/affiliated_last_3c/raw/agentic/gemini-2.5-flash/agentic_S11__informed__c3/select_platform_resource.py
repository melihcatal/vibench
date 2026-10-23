import vertexai
import os


def select_platform_resource(project_id: str, location: str, model_id: str):
    vertexai.init(project=project_id, location=location)
    # In Vertex AI, selecting a model often means getting a reference to it.
    # The GenerativeModel class handles this internally.
    # For this example, we'll just return the model_id if it's considered 'available'.
    # A more complex scenario might involve listing available models and filtering.
    print(
        f"Selected Vertex AI model: {model_id} in project {project_id}, location {location}"
    )
    return model_id


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_id = os.environ.get("VERTEX_AI_MODEL_ID", "gemini-pro")
    if project_id:
        selected_model = select_platform_resource(project_id, location, model_id)
        print(f"Resource selected: {selected_model}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
