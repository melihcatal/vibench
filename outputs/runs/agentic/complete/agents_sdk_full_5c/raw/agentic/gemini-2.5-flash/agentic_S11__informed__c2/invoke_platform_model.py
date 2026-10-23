import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def invoke_model(project_id: str, location: str, model_id: str, prompt: str) -> str:
    """Invokes a Vertex AI model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (replace with your actual project, location, and model)
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro"
    prompt = "What is the capital of France?"
    
    # print(f"Invoking model {model_id} in project {project_id}...")
    # try:
    #     result = invoke_model(project_id, location, model_id, prompt)
    #     print("Model output:", result)
    # except Exception as e:
    #     print(f"Error invoking model: {e}")
