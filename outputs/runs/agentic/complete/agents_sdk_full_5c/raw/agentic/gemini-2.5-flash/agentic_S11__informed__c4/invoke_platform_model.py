import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def invoke_platform_model(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us-central1"
    model_name = "gemini-pro"
    prompt = "Tell me a story about a brave knight."
    output = invoke_platform_model(project_id, location, model_name, prompt)
    print(f"Model output: {output}")
