import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def collect_metadata(project_id: str, location: str, model_name: str, prompt: str):
    """Returns model output together with Vertex AI platform metadata."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content([Part.from_text(prompt)])
    
    output_text = response.text
    metadata = {}
    if response.usage_metadata:
        metadata = {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        }
    
    # In a real scenario, you might also include response.candidates[0].finish_reason if available
    # or other specific attributes from the raw response object.

    return {"output": output_text, "metadata": metadata}

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_name = "gemini-pro" # Provider-specific model ID
    prompt = "Summarize the key benefits of cloud computing in one paragraph."
    if project_id:
        result = collect_metadata(project_id, location, model_name, prompt)
        print(f"Model Output: {result["output"]}")
        print(f"Platform Metadata: {result["metadata"]}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
