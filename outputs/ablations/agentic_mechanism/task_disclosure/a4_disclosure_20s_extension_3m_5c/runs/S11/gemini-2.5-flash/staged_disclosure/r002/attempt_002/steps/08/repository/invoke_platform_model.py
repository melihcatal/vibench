import vertexai
from vertexai.preview.generative_models import GenerativeModel

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    """Invokes a provider-managed model through a platform client."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Replace with your Google Cloud Project ID and desired location
    PROJECT_ID = "your-gcp-project-id"  # e.g., "my-gcp-project"
    LOCATION = "us-central1"
    MODEL_NAME = "gemini-pro"
    PROMPT = "What is the capital of France?"

    if PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
    else:
        try:
            result = invoke_model(PROJECT_ID, LOCATION, MODEL_NAME, PROMPT)
            print(f"Model Response: {result}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Ensure you have authenticated with 'gcloud auth application-default login' and enabled the Vertex AI API in your project.")
