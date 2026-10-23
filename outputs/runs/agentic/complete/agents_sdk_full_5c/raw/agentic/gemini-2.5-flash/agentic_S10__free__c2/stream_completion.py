import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import init_vertex_ai, get_generative_model
from typing import Iterator

# Vertex AI provider-identifying signal: vertexai import, GenerativeModel class, "gemini-pro" model ID

def stream_completion(prompt: str, project_id: str, location: str = "us-central1") -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM (Vertex AI Gemini Pro).
    """
    init_vertex_ai(project_id=project_id, location=location)
    model = get_generative_model("gemini-pro") # Concrete model ID

    responses = model.generate_content(prompt, stream=True)
    
    for response in responses:
        yield response.text

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    sample_prompt = "Write a short story about a brave knight and a dragon, starting with 'Once upon a time...'"
    
    print("Streaming story completion:")
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder.
    for chunk in stream_completion(sample_prompt, project_id="your-gcp-project-id"):
        print(chunk, end="")
    print("\n[Stream Finished]")
