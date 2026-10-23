import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    """Invokes a Vertex AI generative model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content([Part.from_text(prompt)])
    return response.text

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_name = "gemini-pro" # Provider-specific model ID
    prompt = "Tell me a short story about a brave knight."
    if project_id:
        result = invoke_model(project_id, location, model_name, prompt)
        print(f"Model Output: {result}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
