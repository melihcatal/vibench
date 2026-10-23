import os
import vertexai
from vertexai.language_models import TextGenerationModel

def select_model_resource(project_id: str, location: str, model_id: str):
    """Resolves and returns a Vertex AI text generation model resource."""
    vertexai.init(project=project_id, location=location)
    # Using from_pretrained to resolve a specific model resource
    model = TextGenerationModel.from_pretrained(model_id)
    return model

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_id = "text-bison" # Provider-specific model ID
    if project_id:
        model_resource = select_model_resource(project_id, location, model_id)
        print(f"Selected Model Resource: {model_resource.model_name}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
