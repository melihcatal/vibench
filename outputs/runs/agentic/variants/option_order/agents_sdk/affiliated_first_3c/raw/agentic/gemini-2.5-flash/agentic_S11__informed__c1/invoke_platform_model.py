import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    """Invokes a Vertex AI managed model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (replace with your project and location)
    # response = invoke_model("your-gcp-project-id", "us-central1", "gemini-pro", "Hello, how are you?")
    # print(response)
    pass
