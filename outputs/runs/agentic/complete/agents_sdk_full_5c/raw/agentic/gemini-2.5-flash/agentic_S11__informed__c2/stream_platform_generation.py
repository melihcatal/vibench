import vertexai
from vertexai.preview.generative_models import GenerativeModel

def stream_generation(project_id: str, location: str, model_id: str, prompt: str):
    """
    Streams output from a Vertex AI model.
    
    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region.
        model_id: The ID of the model to use (e.g., "gemini-pro").
        prompt: The text prompt for the model.
        
    Yields:
        str: Chunks of the streamed text output.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    responses = model.generate_content(prompt, stream=True)
    
    for response in responses:
        if response.text:
            yield response.text

if __name__ == '__main__':
    # Example usage
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro"
    prompt = "Tell me a short story about a brave knight and a dragon."

    # print(f"Streaming generation from {model_id} in {project_id}...")
    # try:
    #     full_story = ""
    #     for chunk in stream_generation(project_id, location, model_id, prompt):
    #         print(chunk, end="")
    #         full_story += chunk
    #     print("\n\nStream complete.")
    # except Exception as e:
    #     print(f"Error streaming generation: {e}")
