import vertexai
from vertexai.generative_models import GenerativeModel, Part

def collect_metadata(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    
    output_text = response.text
    
    # For Vertex AI, usage metadata is available on the response object
    # The exact structure might vary, but this shows where to look.
    metadata = {
        "model": model_name,
        "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
        "candidates_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
        "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else None,
        # Add other relevant metadata if available
    }
    
    return output_text, metadata

if __name__ == '__main__':
    # This is an example, replace with your actual project ID and location
    # Also ensure GOOGLE_APPLICATION_CREDENTIALS is set
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_name = "gemini-pro"
    user_prompt = "Summarize the plot of Romeo and Juliet in one sentence."
    
    output, metadata = collect_metadata(project_id, location, model_name, user_prompt)
    
    print(f"Generated Output: {output}")
    print(f"Platform Metadata: {metadata}")
