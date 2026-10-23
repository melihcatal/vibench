import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def stream_generation(project_id: str, location: str, model_name: str, prompt: str):
    """Streams output from a Vertex AI generative model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content([Part.from_text(prompt)], stream=True)
    
    full_response = ""
    for response in responses:
        # Preserve provider response objects (yield or process here)
        # For demonstration, we'll just print the text parts.
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            full_response += part.text
                            # In a real scenario, you might yield 'response' object itself
                            # or a processed part of it.
    return full_response

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_name = "gemini-pro" # Provider-specific model ID
    prompt = "Write a very long, detailed description of a futuristic city and its inhabitants. Be very verbose."
    if project_id:
        print("Streaming generation from Vertex AI:")
        result = stream_generation(project_id, location, model_name, prompt)
        print(f"\nFull streamed output: {result}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
