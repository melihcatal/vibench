import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def invoke_platform_model(prompt: str, project_id: str, location: str, model_name: str = "gemini-pro") -> str:
    """Invokes a Vertex AI managed model through a project-, deployment-, or inference-profile-scoped platform client."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (replace with your actual project_id and location)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if project_id:
        result = invoke_platform_model("What is the capital of France?", project_id, location)
        print(f"Model response: {result}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
