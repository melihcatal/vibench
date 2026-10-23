import vertexai
from vertexai.generative_models import GenerativeModel, Part

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # This is an example and requires proper project_id, location, and model_name
    # For instance, project_id="your-gcp-project-id", location="us-central1", model_name="gemini-pro"
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up for authentication.
    pass
