import vertexai
from vertexai.generative_models import GenerativeModel, Part

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # This is an example, replace with your actual project ID and location
    # Also ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # https://cloud.google.com/docs/authentication/application-default-credentials
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_name = "gemini-pro"
    user_prompt = "Tell me a short story about a brave knight."
    result = invoke_model(project_id, location, model_name, user_prompt)
    print(f"Generated Text: {result}")
