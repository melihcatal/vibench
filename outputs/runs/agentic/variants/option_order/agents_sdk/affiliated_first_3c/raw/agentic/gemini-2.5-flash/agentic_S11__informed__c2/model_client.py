import os
import vertexai
from vertexai.generative_models import GenerativeModel

class VertexAIModelClient:
    def __init__(self, project_id: str = None, location: str = None, model_name: str = "gemini-pro"):
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self.location = location or os.getenv("GCP_LOCATION", "us-central1")
        self.model_name = model_name
        
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID environment variable or project_id parameter must be set.")

        vertexai.init(project=self.project_id, location=self.location)
        self._model = GenerativeModel(self.model_name)

    def get_model(self) -> GenerativeModel:
        return self._model
    
    def generate_content(self, prompt: str, stream: bool = False):
        if stream:
            return self._model.generate_content(prompt, stream=True)
        else:
            return self._model.generate_content(prompt)

if __name__ == '__main__':
    # Example usage:
    # client = VertexAIModelClient(project_id="your-gcp-project-id", model_name="gemini-pro")
    # model = client.get_model()
    # response = client.generate_content("What is the capital of France?")
    # print(response.text)
    pass
