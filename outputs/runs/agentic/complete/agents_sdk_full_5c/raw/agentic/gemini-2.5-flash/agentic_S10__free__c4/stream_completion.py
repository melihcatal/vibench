import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os

def stream_completion(prompt: str):
    """Streams partial output tokens from a hosted LLM."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Gemini models support streaming
    
    responses = model.generate_content(
        [Part.from_text(prompt)],
        stream=True
    )
    
    # This generator yields chunks of text as they become available
    for response in responses:
        yield response.text
