from google import genai
from model_models import ModelRequest

def stream_platform_generation(model_request: ModelRequest):
    project_id = model_request.config.get("project_id")
    location = model_request.config.get("location")
    model_name = model_request.config.get("model_name", "gemini-2.5-flash")

    # Initialize the generative AI client for Vertex AI
    client = genai.Client(vertexai=True, project=project_id, location=location)
    model = client.get_model(model_name)

    # Stream the content generation
    responses = model.generate_content(model_request.text, stream=True)
    
    for response in responses:
        # Each 'response' object from the stream can be yielded directly
        # The exact structure depends on the provider's SDK, but this preserves it.
        yield response
