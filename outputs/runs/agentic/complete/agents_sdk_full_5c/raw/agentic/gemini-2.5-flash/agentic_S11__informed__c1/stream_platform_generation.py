import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def stream_platform_generation(prompt: str, project_id: str, location: str, model_name: str = "gemini-pro"):
    """Streams output from a managed model platform while preserving provider response objects."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        print(f"Streamed part: {response.text}")
        # 'response' is the provider's response object

if __name__ == '__main__':
    # Example usage (replace with your actual project_id and location)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if project_id:
        print("Streaming response for 'Tell me a story about a brave knight and a dragon':")
        stream_platform_generation("Tell me a story about a brave knight and a dragon.", project_id, location)
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
