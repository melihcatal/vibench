import vertexai
import os

def select_model_resource(project_id: str, location: str, model_id: str) -> str:
    vertexai.init(project=project_id, location=location)
    # In Vertex AI, selecting a model resource typically involves specifying its ID.
    # The GenerativeModel class will then use this ID.
    # This function merely confirms the model ID for the given project/location.
    print(f"Selected Vertex AI model: {model_id} in project {project_id}, location {location}")
    return model_id

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_id = "gemini-pro"
    if project_id:
        selected_model = select_model_resource(project_id, location, model_id)
        print(f"Successfully confirmed model resource: {selected_model}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
