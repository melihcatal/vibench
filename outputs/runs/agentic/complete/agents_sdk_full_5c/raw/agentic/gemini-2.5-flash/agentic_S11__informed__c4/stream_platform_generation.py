import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def stream_platform_generation(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    
    for response in responses:
        # Each 'response' object here is a provider response object.
        # We can extract text or other details as needed.
        yield {"text": response.text, "raw_response_object": response}

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us-central1"
    model_name = "gemini-pro"
    prompt = "Write a very long, detailed story about a space explorer's journey to a new galaxy."
    print("Streaming generation:")
    for chunk in stream_platform_generation(project_id, location, model_name, prompt):
        print(chunk["text"], end="")
