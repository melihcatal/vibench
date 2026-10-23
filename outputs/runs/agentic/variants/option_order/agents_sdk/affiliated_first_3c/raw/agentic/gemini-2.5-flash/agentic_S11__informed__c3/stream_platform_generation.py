import vertexai
from vertexai.generative_models import GenerativeModel
import os

def stream_generation(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        print(f"Streamed content: {response.text}")
        # Preserve the full response object if needed
        yield response

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_name = "gemini-pro"
    prompt = "Write a very long, detailed description of a futuristic city.\n\n"
    if project_id:
        print("Starting streaming generation...")
        for response_obj in stream_generation(project_id, location, model_name, prompt):
            # You can access more details from response_obj if required
            pass
        print("Streaming generation complete.")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
