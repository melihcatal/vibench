import vertexai
from vertexai.generative_models import GenerativeModel

def collect_metadata(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    
    metadata = {
        "text": response.text,
        "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
        "candidates_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
        "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None,
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
        # Add other relevant metadata from the response object if available
    }
    return metadata

if __name__ == '__main__':
    # Example usage (requires appropriate project_id, location, model_name)
    # output_with_metadata = collect_metadata("your-gcp-project-id", "us-central1", "gemini-pro", "Hello.")
    # print(output_with_metadata)
    pass
