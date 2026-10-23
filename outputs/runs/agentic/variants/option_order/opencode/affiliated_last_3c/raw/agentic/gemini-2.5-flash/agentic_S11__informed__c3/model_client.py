import vertexai
from vertexai.generative_models import GenerativeModel
import os


class VertexAIModelClient:
    def __init__(self, project_id: str, location: str, model_name: str):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        vertexai.init(project=self.project_id, location=self.location)
        self.model = GenerativeModel(self.model_name)

    def generate_content(self, prompt: str, stream: bool = False):
        return self.model.generate_content(prompt, stream=stream)

    def get_model_name(self):
        return self.model_name


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = os.environ.get("VERTEX_AI_MODEL_NAME", "gemini-pro")
    if project_id:
        client = VertexAIModelClient(project_id, location, model_name)
        print(f"Initialized Vertex AI client for model: {client.get_model_name()}")
        test_prompt = "What is the capital of France?"
        response = client.generate_content(test_prompt)
        print(f"Response: {response.text}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
