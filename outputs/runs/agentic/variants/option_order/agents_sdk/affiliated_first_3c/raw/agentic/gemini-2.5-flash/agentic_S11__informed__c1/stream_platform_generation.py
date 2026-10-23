import vertexai
from vertexai.preview.generative_models import GenerativeModel
from typing import Iterator

def stream_generation(project_id: str, location: str, model_name: str, prompt: str) -> Iterator[str]:
    """Streams output from a Vertex AI managed model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        if response.text:
            yield response.text

if __name__ == '__main__':
    # Example usage
    # print("Streaming generation:")
    # for chunk in stream_generation("your-gcp-project-id", "us-central1", "gemini-pro", "Write a short story about a cat."):
    #     print(chunk, end='')
    # print("\nStream complete.")
    pass
