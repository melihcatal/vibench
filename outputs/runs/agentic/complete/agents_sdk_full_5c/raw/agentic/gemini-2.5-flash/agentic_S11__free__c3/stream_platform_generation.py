from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1.types import content as gapic_content
import json

def stream_vertex_generation(project_id: str, location: str, model_id: str, prompt: str):
    """Streams output from a Vertex AI model while preserving provider response objects."""
    # For streaming, we typically use the v1beta1 client and stream_generate_content for Gemini models.
    client = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    
    # The endpoint for streaming is usually in the format: projects/PROJECT_ID/locations/LOCATION/publishers/google/models/MODEL_ID
    # For gemini-pro, it's publishers/google/models/gemini-pro
    publisher_model = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    contents = [gapic_content.Content(parts=[gapic_content.Part(text=prompt)])]

    # Provider-identifying signal: google.cloud.aiplatform.PredictionServiceClient and model_id like 'gemini-pro'
    # and the specific stream_generate_content method.

    stream = client.stream_generate_content(model=publisher_model, contents=contents)

    for response in stream:
        # The response object is a GenerateContentResponse from aiplatform_v1beta1.types
        yield response

if __name__ == '__main__':
    # Example usage (replace with your actual project and location)
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro"
    prompt = "Write a very short poem about the ocean, streaming word by word."

    print(f"Streaming generation from {model_id}:")
    full_response_text = ""
    for response_object in stream_vertex_generation(project_id, location, model_id, prompt):
        # Accessing the text from the response object
        if response_object.candidates:
            for part in response_object.candidates[0].content.parts:
                if part.text:
                    print(part.text, end='')
                    full_response_text += part.text
    print(f"\n\nFull streamed response accumulated: {full_response_text}")
