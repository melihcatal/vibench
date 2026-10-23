import os
import vertexai
from vertexai.generative_models import GenerativeModel

def select_platform_resource(project_id: str, location: str, model_name: str = "gemini-pro") -> GenerativeModel:
    """Resolves a provider-specific model, deployment, or inference resource before invocation."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    return model

if __name__ == '__main__':
    # Example usage (replace with your actual project_id and location)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if project_id:
        model_resource = select_platform_resource(project_id, location)
        print(f"Selected Vertex AI GenerativeModel resource: {model_resource.model_name}")
        # You can then use this resource to generate content
        # response = model_resource.generate_content("Hello there!")
        # print(response.text)
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
