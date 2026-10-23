import vertexai
from vertexai.generative_models import GenerativeModel, Part

def stream_generation(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    
    for response in responses:
        yield response # Yield the raw provider response object

if __name__ == '__main__':
    # Example usage (requires appropriate project_id, location, model_name)
    # for chunk in stream_generation("your-gcp-project-id", "us-central1", "gemini-pro", "Write a long story."):
    #     print(chunk.text, end='')
    pass
