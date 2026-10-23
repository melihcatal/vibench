import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def collect_platform_metadata(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    
    metadata = {
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
    }
    
    # Vertex AI GenerativeModel responses might contain usage metadata
    if hasattr(response, 'usage_metadata'):
        metadata["usage_metadata"] = {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        }
    
    return {"text": response.text, "platform_metadata": metadata}

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us-central1"
    model_name = "gemini-pro"
    prompt = "What is the capital of France?"
    output_with_metadata = collect_platform_metadata(project_id, location, model_name, prompt)
    print(f"Model output: {output_with_metadata["text"]}")
    print(f"Platform metadata: {output_with_metadata["platform_metadata"]}")
