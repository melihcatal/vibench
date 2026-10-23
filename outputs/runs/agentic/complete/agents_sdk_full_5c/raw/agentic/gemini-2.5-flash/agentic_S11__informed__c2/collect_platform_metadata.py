import vertexai
from vertexai.preview.generative_models import GenerativeModel

def collect_platform_metadata(project_id: str, location: str, model_id: str, prompt: str) -> dict:
    """
    Invokes a Vertex AI model and collects output along with platform metadata.
    
    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region.
        model_id: The ID of the model to use (e.g., "gemini-pro").
        prompt: The text prompt for the model.
        
    Returns:
        A dictionary containing the model output and platform metadata.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    response = model.generate_content(prompt)
    
    metadata = {
        "text": response.text,
        "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
        "token_count": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
        "model_id": model_id,
        "project_id": project_id,
        "location": location
    }
    return metadata

if __name__ == '__main__':
    # Example usage
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro"
    prompt = "Summarize the main plot of the movie Inception."

    # print(f"Collecting metadata from {model_id} in {project_id}...")
    # try:
    #     result_with_metadata = collect_platform_metadata(project_id, location, model_id, prompt)
    #     print("Model output:", result_with_metadata.get("text"))
    #     print("Metadata:", {k: v for k, v in result_with_metadata.items() if k != "text"})
    # except Exception as e:
    #     print(f"Error collecting platform metadata: {e}")
