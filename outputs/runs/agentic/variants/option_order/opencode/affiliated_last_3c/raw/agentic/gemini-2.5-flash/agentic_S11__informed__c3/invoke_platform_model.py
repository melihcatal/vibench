import vertexai
from vertexai.generative_models import GenerativeModel
import os


def invoke_platform_model(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = os.environ.get("VERTEX_AI_MODEL_NAME", "gemini-pro")
    test_prompt = "Hello, what is your name?"
    if project_id:
        print(f"Invoking Vertex AI model {model_name}...")
        output = invoke_platform_model(project_id, location, model_name, test_prompt)
        print(f"Model Output: {output}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
