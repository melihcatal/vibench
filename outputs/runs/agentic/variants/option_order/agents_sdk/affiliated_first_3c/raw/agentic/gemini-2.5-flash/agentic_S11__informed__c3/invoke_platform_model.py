import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
import os

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage (replace with your actual project_id and location)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_name = "gemini-pro"
    prompt = "Tell me a story about a brave knight."
    if project_id:
        output = invoke_model(project_id, location, model_name, prompt)
        print(f"Model Output: {output}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
