import vertexai
from vertexai.generative_models import GenerativeModel, Part

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    import os
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_name = "gemini-pro" # Provider-specific model ID
    test_prompt = "Tell me a short story about a futuristic city."
    if project_id:
        print(f"Invoking Vertex AI model {model_name}...")
        output = invoke_model(project_id, location, model_name, test_prompt)
        print("Model Output:", output)
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
