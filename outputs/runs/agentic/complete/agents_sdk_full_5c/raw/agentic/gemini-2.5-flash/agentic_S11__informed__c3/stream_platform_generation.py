import vertexai
from vertexai.generative_models import GenerativeModel

def stream_generation(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        # The response object from Vertex AI is preserved.
        # Accessing .text gives the string content.
        yield response

if __name__ == '__main__':
    # This is an example, replace with your actual project ID and location
    # Also ensure GOOGLE_APPLICATION_CREDENTIALS is set
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_name = "gemini-pro"
    user_prompt = "Write a very long, detailed story about a space explorer's first encounter with an alien species."

    print("Streaming generation:")
    full_response_text = ""
    for part in stream_generation(project_id, location, model_name, user_prompt):
        if part.text:
            print(part.text, end='')
            full_response_text += part.text
    print("\n\nStreaming complete.")
    # You can access metadata from the individual 'part' objects if needed
    # e.g., print(part.usage_metadata) if available in streaming parts
